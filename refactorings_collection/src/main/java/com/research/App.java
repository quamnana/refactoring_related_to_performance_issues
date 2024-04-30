package com.research;

public class App {

    public static void main(String[] args) {

        DbHelpers db = new DbHelpers();
        ExtractRefactorings extractRef = new ExtractRefactorings();
        db.establishDBConnection();
        extractRef.extractPUllRequestRefs();

    }

}
