package no.tim.cardsearch.search


import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RequestParam
import org.springframework.web.bind.annotation.RestController
import kotlin.math.min

@RestController
@RequestMapping("/search")
class SearchController(
    private val cardDataService: CardDataService
) {

    fun levenshtein(a: String, b: String): Int {
        val dp = Array(a.length + 1) { IntArray(b.length + 1) }
        for (i in 0..a.length) dp[i][0] = i
        for (j in 0..b.length) dp[0][j] = j
        for (i in 1..a.length) {
            for (j in 1..b.length) {
                dp[i][j] = if (a[i - 1] == b[j - 1]) dp[i - 1][j - 1]
                else min(min(dp[i - 1][j], dp[i][j - 1]), dp[i - 1][j - 1]) + 1
            }
        }
        return dp[a.length][b.length]
    }

    @GetMapping("")
    fun searchCards(
        @RequestParam query: String,
        @RequestParam(required = false, defaultValue = "20") limit: Int,
        @RequestParam(required = false, defaultValue = "0") page: Int
    ): Map<String, Map<String, CardPriceObject>?> {
        val normalizedQuery = query.replace(Regex("[^A-Za-z0-9 ]"), "").lowercase()
        val nameEntries = cardDataService.getNormalizedNameEntries()
        val maxDistance = 2
        val prioritized = nameEntries
            .filter { it.normalized.contains(normalizedQuery) ||
                it.words.any { word -> levenshtein(word, normalizedQuery) <= maxDistance }
            }
            .sortedWith(compareBy(
                { entry ->
                    val idx = entry.words.indexOfFirst { word -> word.startsWith(normalizedQuery) }
                    if (idx == -1) Int.MAX_VALUE else idx
                },
                { entry ->
                    entry.words.minOfOrNull { word -> levenshtein(word, normalizedQuery) } ?: Int.MAX_VALUE
                },
                { entry -> entry.original }
            ))
        val paged = prioritized.drop(page * limit).take(limit)
        return paged.map { it.original }.associateWith { cardDataService.getPriceData(it) }
    }
}