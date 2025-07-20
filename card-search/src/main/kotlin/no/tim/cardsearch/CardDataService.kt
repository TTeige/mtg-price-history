package no.tim.cardsearch

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

    @PostConstruct
    fun initCache() {
        getCardData()
    }

    @Scheduled(cron = "0 0 12 * * *")
    fun invalidateCacheMorning() {
        cache.clear()
        getCardData()
    }

    @Scheduled(cron = "0 0 0 * * *")
    fun invalidateCacheEvening() {
        cache.clear()
        getCardData()
    }

    private fun getLatestPriceFileKey(): String? {
        val s3Client = AmazonS3ClientBuilder.defaultClient()
        val objects = s3Client.listObjects(bucketName, "prices/").objectSummaries
        val latest = objects.maxByOrNull { it.lastModified }
        return latest?.key
    }

    fun getCardData(): Map<String, Map<String, CardPriceObject>> {
        if (cache.isEmpty()) {
            val s3Client = AmazonS3ClientBuilder.defaultClient()
            val latestKey = getLatestPriceFileKey() ?: key
            val s3Object: S3Object = s3Client.getObject(bucketName, latestKey)
            val json = s3Object.objectContent.bufferedReader().use { it.readText() }
            val data: Map<String, Map<String, CardPriceObject>> = objectMapper.readValue(json,
                object: TypeReference<Map<String, Map<String, CardPriceObject>>>() { }
            )
            cache.putAll(data)
        }
        return cache
    }
}
