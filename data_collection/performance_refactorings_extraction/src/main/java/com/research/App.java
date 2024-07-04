package com.research;

public class App {

    public static void main(String[] args) {

        DBHelpers db = new DBHelpers();
        RefactoringExtraction extractRef = new RefactoringExtraction();
        db.establishDBConnection();
        extractRef.getPerformanceRefactorings();

    }

}
