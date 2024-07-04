# Use an official OpenJDK runtime as a parent image
FROM openjdk:17-jdk-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# If you're using Maven to build your project, you can add these lines to build the project
# and package it. Uncomment the lines below if needed.
RUN apt-get update && apt-get install -y maven
RUN mvn clean package

# Alternatively, if you already have a JAR file built, just copy it into the container
# COPY target/your-app.jar /app/your-app.jar

# Make port 8080 available to the world outside this container
# EXPOSE 8080

# Run the application
CMD ["java", "src/main/java/com/research/App.java"]
