package no.tim.cardsearch

import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RequestParam
import org.springframework.web.bind.annotation.RestController

@RestController
@RequestMapping("/search")
class SearchController(
    private val cardDataService: CardDataService
) {

    @GetMapping("")
    fun searchCards(
        @RequestParam query: String,
        @RequestParam(required = false, defaultValue = "20") limit: Int,
        @RequestParam(required = false, defaultValue = "0") page: Int
    ): List<String> {
        val normalizedQuery = query.replace(Regex("[^A-Za-z0-9 ]"), "").lowercase()
        val nameEntries = cardDataService.getNormalizedNameEntries()
        val prioritized = nameEntries
            .filter { it.normalized.contains(normalizedQuery) }
            .sortedWith(compareBy(
                { entry ->
                    val idx = entry.words.indexOfFirst { word -> word.startsWith(normalizedQuery) }
                    if (idx == -1) Int.MAX_VALUE else idx
                },
                { entry -> entry.original }
            ))
        val paged = prioritized.drop(page * limit).take(limit)
        return paged.map { it.original }
    }
}