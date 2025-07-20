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
    fun searchCards(@RequestParam query: String): Map<String, Map<String, CardPriceObject>> {
        val cardData = cardDataService.getCardData()
        // Normalize query and keys: remove special characters and compare case-insensitive
        val normalizedQuery = query.replace(Regex("[^A-Za-z0-9 ]"), "").lowercase()
        return cardData.filterKeys {
            it.replace(Regex("[^A-Za-z0-9 ]"), "").lowercase().contains(normalizedQuery)
        }
    }
}