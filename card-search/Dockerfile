FROM eclipse-temurin:17-jre

WORKDIR /app

COPY build/libs/cardsearch-0.0.2-SNAPSHOT.jar app.jar

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]

