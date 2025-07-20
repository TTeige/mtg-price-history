package no.tim.cardsearch

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication

@SpringBootApplication
class CardSearchApplication

fun main(args: Array<String>) {
    runApplication<CardSearchApplication>(*args)
}
