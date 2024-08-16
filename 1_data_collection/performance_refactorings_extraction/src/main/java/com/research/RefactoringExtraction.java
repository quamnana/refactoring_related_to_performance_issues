package com.research;

import java.io.FileWriter;
import java.io.IOException;
import java.util.List;
import java.io.File;

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
    String issuesCollectionName = "performance-issues";
    String projectsCollectionName = "all-projects";
    String performanceRefCollectionName = "all-performance-refactorings";

    public void getPerformanceRefactorings() {
        final String errorLogsFilePath = "./logs/perf/error.log";
        int counter = 0;
        FindIterable<Document> issues = db.getAllDataFromDB(issuesCollectionName);
        long total = db.countData(issuesCollectionName);

        for (Document issue : issues) {
            counter++;

            Integer prNumber = issue.getInteger("pr_number");
            System.out.println("========================= GETTING REFATORING ======================= (" + counter + "/"
                    + total + ")");
            if (prNumber != null) {
                getRefactoringsByPullRequest(issue, errorLogsFilePath);
            } else {
                continue;
            }

        }
    }

    /**
     * Retrieves refactorings associated with a given pull request.
     *
     * @param issue             A MongoDB document containing information about the
     *                          issue, including repository details,
     *                          pull request number, performance and bug keywords,
     *                          issue number, and title.
     * @param errorLogsFilePath The file path where error logs will be written.
     *
     * @throws Exception If an error occurs during the retrieval or logging of
     *                   refactorings.
     */

    private void getRefactoringsByPullRequest(Document issue, String errorLogsFilePath) {
        final String repoName = issue.getString("repo_name");
        final String repoFullName = issue.getString("repo_fullname");
        final String repoUrl = issue.getString("repo_url") + ".git";
        final int prNumber = issue.getInteger("pr_number");
        final String perfKeyword = issue.getString("perf_keyword");
        final String bugKeyword = issue.getString("bug_keyword");
        final int issueNumber = issue.getInteger("issue_number");
        final String issueTitle = issue.getString("issue_title");

        final String[] commitWithError = { null };
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

    /**
     * Initializes a Git repository at the specified file path using the provided
     * GitHub URL.
     * If the repository already exists at the file path, it will be fetched from
     * the remote.
     * If the repository does not exist, it will be cloned from the remote.
     *
     * @param projectFilePath  The file path where the repository will be
     *                         initialized.
     * @param projectGithubUrl The GitHub URL of the repository.
     *
     * @return The initialized Git repository.
     *
     * @throws Exception If an error occurs during the cloning or fetching of the
     *                   repository.
     */
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
