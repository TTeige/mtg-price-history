package no.tim.cardsearch.search

import com.amazonaws.services.s3.AmazonS3ClientBuilder
import com.amazonaws.services.s3.model.S3Object
import com.fasterxml.jackson.core.type.TypeReference
import com.fasterxml.jackson.module.kotlin.jacksonObjectMapper
import jakarta.annotation.PostConstruct
import org.springframework.scheduling.annotation.Scheduled
import org.springframework.stereotype.Service
import java.util.concurrent.ConcurrentHashMap

@Service
class CardDataService {
    private val cache = ConcurrentHashMap<String, Map<String, CardPriceObject>>()
    private val objectMapper = jacksonObjectMapper()
    private val bucketName = "mtg-pricing-data"
    private val key = "prices/price_data_2025-07-17-09.json"
    private val normalizedNameCache: MutableList<NameEntry> = mutableListOf()

    @PostConstruct
    fun initCache() {
        buildCardCaches()
    }

    @Scheduled(cron = "0 0 12 * * *")
    fun invalidateCacheMorning() {
        cache.clear()
        buildCardCaches()
    }

    @Scheduled(cron = "0 0 0 * * *")
    fun invalidateCacheEvening() {
        cache.clear()
        buildCardCaches()
    }

    private fun getLatestPriceFileKey(): String? {
        val s3Client = AmazonS3ClientBuilder.defaultClient()
        val objects = s3Client.listObjects(bucketName, "prices/").objectSummaries
        val latest = objects.maxByOrNull { it.lastModified }
        return latest?.key
    }

    fun buildCardCaches(): Map<String, Map<String, CardPriceObject>> {
        if (cache.isEmpty()) {
            val s3Client = AmazonS3ClientBuilder.defaultClient()
            val latestKey = getLatestPriceFileKey() ?: key
            val s3Object: S3Object = s3Client.getObject(bucketName, latestKey)
            val json = s3Object.objectContent.bufferedReader().use { it.readText() }
            val data: Map<String, Map<String, CardPriceObject>> = objectMapper.readValue(json,
                object: com.fasterxml.jackson.core.type.TypeReference<Map<String, Map<String, CardPriceObject>>>() { }
            )
            cache.putAll(data)
            normalizedNameCache.clear()
            normalizedNameCache.addAll(data.keys.map { name ->
                val normalized = name.replace(Regex("[^A-Za-z0-9 ]"), "").lowercase()
                val words = name.split(" ").map { it.replace(Regex("[^A-Za-z0-9]"), "").lowercase() }
                NameEntry(name, normalized, words)
            })
        }
        return cache
    }

    fun getNormalizedNameEntries(): List<NameEntry> {
        if (normalizedNameCache.isEmpty()) {
            buildCardCaches() // This will populate normalizedNameCache as well
        }
        return normalizedNameCache
    }

    data class NameEntry(val original: String, val normalized: String, val words: List<String>)
}
