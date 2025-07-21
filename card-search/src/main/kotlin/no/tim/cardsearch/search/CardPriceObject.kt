package no.tim.cardsearch.search

import com.fasterxml.jackson.annotation.JsonProperty


data class CardPriceObject(
    @JsonProperty("multiverse_ids")
    val multiverseIds: List<Int>,
    @JsonProperty("name")
    val name: String,
    @JsonProperty("set")
    val set: String,
    @JsonProperty("set_name")
    val setName: String,
    @JsonProperty("prices")
    val prices: Map<String, String?>,
    @JsonProperty("purchase_uris")
    val purchaseUris: Map<String, String>,
    @JsonProperty("image_uri")
    val imageUri: String?
)
