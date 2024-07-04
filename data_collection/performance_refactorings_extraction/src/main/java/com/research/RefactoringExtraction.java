package com.research;

import java.io.FileWriter;
import java.io.IOException;
import java.util.List;

import org.eclipse.jgit.lib.Repository;
import org.refactoringminer.api.GitHistoryRefactoringMiner;
import org.refactoringminer.api.GitService;
import org.refactoringminer.api.Refactoring;
import org.refactoringminer.api.RefactoringHandler;
import org.refactoringminer.rm1.GitHistoryRefactoringMinerImpl;
import org.refactoringminer.util.GitServiceImpl;

import com.mongodb.client.FindIterable;
import org.bson.Document;

public class RefactoringExtraction {
    GitService gitService = new GitServiceImpl();
    GitHistoryRefactoringMiner miner = new GitHistoryRefactoringMinerImpl();
    DBHelpers db = new DBHelpers();
    String issuesCollectionName = "performance-issues-20stars";
    String projectsCollectionName = "projects";
    String performanceRefCollectionName = "performance-refactorings-20stars";
    String nonPerformanceRefCollectionName = "non-performance-refactorings";

    public void getPerformanceRefactorings() {
        final String errorLogsFilePath = "./logs/perf/error.log";
        int counter = 0;
        FindIterable<Document> issues = db.getAllDataFromDB(issuesCollectionName);
        long total = db.countData(issuesCollectionName);

        for (Document issue : issues) {
            counter++;
            if (counter < 101) {
                continue;
            }
            Integer prNumber = issue.getInteger("pr_number");
            System.out.println("========================= GETTING REFATORINGS ======================= (" + counter + "/"
                    + total + ")");
            if (prNumber != null) {
                getRefactoringsByPullRequest(issue, errorLogsFilePath);
            } else {
                continue;
            }

        }
    }

    // public void getNonPerformanceRefactorings() {
    // final String errorLogsFilePath = "./logs/non-perf/error.log";
    // int counter = 0;
    // FindIterable<Document> projects =
    // db.getAllDataFromDB(projectsCollectionName);
    // long total = db.countData(projectsCollectionName);

    // for (Document project : projects) {

    // counter++;
    // // if (counter < 128) {
    // // continue;
    // // }

    // String projectName = project.getString("name");
    // String projectFilePath = "./projects/" + projectName;
    // String githubUrl = project.getString("html_url");
    // String branch = (String) project.getString("default_branch");

    // System.out
    // .println("========================= GETTING REFATORINGS
    // ====================== - " + projectName
    // + " - (" + counter + "/"
    // + total + ")");
    // try {
    // Repository repo = initializeRepo(projectFilePath, githubUrl);
    // getAllRefactorings(repo, projectName, branch, errorLogsFilePath);
    // } catch (Exception e) {
    // // TODO: handle exception
    // continue;
    // }

    // }

    // }

    private void getRefactoringsByPullRequest(Document issue, String errorLogsFilePath) {
        final String repoName = issue.getString("repo_name");
        final String repoFullName = issue.getString("repo_fullname");
        final String repoUrl = issue.getString("repo_url") + ".git";
        final int prNumber = issue.getInteger("pr_number");
        final String perfKeyword = issue.getString("perf_keyword");
        final String bugKeyword = issue.getString("bug_keyword");
        final int issueNumber = issue.getInteger("issue_number");
        final String issueTitle = issue.getString("issue_title");

        final String[] commitWithError = { null }; // Using a final array to hold
        try {
            miner.detectAtPullRequest(repoUrl, prNumber, new RefactoringHandler() {
                @Override
                public void handle(String commitId, List<Refactoring> refactorings) {
                    try {
                        System.out
                                .println("Refactorings for " + repoName + " at PR#" + prNumber + " Commit ID:"
                                        + commitId);
                        commitWithError[0] = commitId; // Assign the current commit ID
                        for (Refactoring ref : refactorings) {
                            System.out.println(ref.toString());
                            Document data = Document.parse(ref.toJSON()).append("commit_id",
                                    commitId).append("repo_name", repoName).append("repo_fullname", repoFullName)
                                    .append("pr_number", prNumber)
                                    .append("perf_keyword", perfKeyword).append("bug_keyword", bugKeyword)
                                    .append("issue_number", issueNumber).append("issue_title", issueTitle);
                            db.persistToDB(performanceRefCollectionName, data);
                        }
                    } catch (Exception e) {
                        // TODO: handle exception
                        System.out.println(
                                "An error occurred during the collection of refactorings inner for commit: "
                                        + commitWithError[0]);

                    }

                }
            }, 100);
        } catch (Exception e) {
            // Log the commit ID causing the exception to a file
            logCommitErrorToFile(commitWithError[0], (String) repoName, errorLogsFilePath);
            System.out.println(
                    "An error occurred during the collection of refactorings for commit: " + commitWithError[0]);
            System.out.println("Error message: " + e.getMessage());
            e.printStackTrace(); // Print stack trace for debugging
        }
    }

    public Repository initializeRepo(String projectFilePath, String projectGithubUrl) {
        try {
            // Code that may throw an exception
            Repository repo = gitService.cloneIfNotExists(projectFilePath, projectGithubUrl);
            return repo;
        } catch (Exception e) {
            // Exception handling code: Add a logger
            System.out.println("An error occured during the cloning of the project: " + e.getMessage());
        }
        return null;
    }

    // private void getAllRefactorings(Repository repo, String projectName, String
    // branch, String errorLogsFilePath) {
    // // final List<Document> refactoringDocs = new ArrayList<>();
    // final String project = projectName;
    // final String[] commitWithError = { null }; // Using a final array to hold the
    // commit ID
    // try {
    // miner.detectAll(repo, branch, new RefactoringHandler() {
    // @Override
    // public void handle(String commitId, List<Refactoring> refactorings) {
    // System.out.println("Refactorings at " + commitId);
    // commitWithError[0] = commitId; // Assign the current commit ID to the array

    // for (Refactoring ref : refactorings) {
    // try {
    // Document data = Document.parse(ref.toJSON()).append("project",
    // project).append("commitId",
    // commitId);
    // db.persistToDB(nonPerformanceRefCollectionName, data);
    // } catch (Exception e) {
    // // TODO: handle exception
    // continue;
    // }

    // }

    // }
    // });
    // } catch (Exception e) {
    // // Log the commit ID causing the exception to a file
    // logCommitErrorToFile(commitWithError[0], projectName, errorLogsFilePath);
    // System.out.println(
    // "An error occurred during the collection of refactorings for commit: " +
    // commitWithError[0]);
    // System.out.println("Error message: " + e.getMessage());
    // e.printStackTrace(); // Print stack trace for debugging
    // }
    // }

    private void logCommitErrorToFile(String commitId, String projectName, String filePath) {
        try (FileWriter writer = new FileWriter(filePath, true)) {
            writer.write("Error occurred for commit: " + commitId + " at " + projectName +
                    "\n");
            // writer.write("Error message: " + exception.getMessage() + "\n");
            writer.write("\n");
        } catch (IOException e) {
            System.out.println("Error occurred while writing to file: " +
                    e.getMessage());
            e.printStackTrace();
        }
    }
}
