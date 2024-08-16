package com.research;

import com.mongodb.client.MongoClients;
import com.mongodb.client.FindIterable;
import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoDatabase;
import com.mongodb.client.MongoCollection;
import org.bson.Document;

public class DBHelpers {
    public static MongoDatabase database;

    public void establishDBConnection() {
        try {

            MongoClient mongoClient = MongoClients.create("mongodb://127.0.0.1:27017/");

            // Connect to the "mydb" database
            database = mongoClient.getDatabase("research");

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void persistToDB(String collectionName, Document data) {
        try {
            // Get a collection
            MongoCollection<Document> collection = database.getCollection(collectionName);

            collection.insertOne(data);
            System.out.println("Successfully persisted data");
        } catch (Exception e) {
            // TODO: handle exception
            System.out.println("Failed to persist data");
            System.out.println(e);
        }

    }

    public FindIterable<Document> getAllDataFromDB(String collectionName) {

        try {
            // Get a collection
            MongoCollection<Document> collection = database.getCollection(collectionName);

            FindIterable<Document> data = collection.find();
            return data;
        } catch (Exception e) {
            // TODO: handle exception
            System.out.println("Failed to fetch data");
            return null;

        }

    }

    public long countData(String collectionName) {

        try {
            // Get a collection
            MongoCollection<Document> collection = database.getCollection(collectionName);

            long count = collection.countDocuments();
            return count;
        } catch (Exception e) {
            // TODO: handle exception
            System.out.println("Failed to count data");
            return 0;

        }

    }

}
