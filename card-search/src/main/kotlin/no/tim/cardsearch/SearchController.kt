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
        val cardData = cardDataService.getCardNames()
        val normalizedQuery = query.replace(Regex("[^A-Za-z0-9 ]"), "").lowercase()
        val filtered = cardData.filter {
            it.replace(Regex("[^A-Za-z0-9 ]"), "").lowercase().contains(normalizedQuery)
        }
        val paged = filtered.drop(page * limit).take(limit)
        return paged
    }
}