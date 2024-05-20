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
import com.mongodb.client.MongoCollection;
import org.bson.Document;

public class ExtractRefactorings {
    GitService gitService = new GitServiceImpl();
    GitHistoryRefactoringMiner miner = new GitHistoryRefactoringMinerImpl();
    DbHelpers db = new DbHelpers();

    public void extractPUllRequestRefs() {

        FindIterable<Document> issues = db.getAllDataFromDB("perf-issues");

        for (Document issue : issues) {
            Integer prNumber = issue.getInteger("pr_number");
            if (prNumber != null) {
                getPullRequestRefactorings(issue);
            } else {
                continue;
            }

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

    public void getPullRequestRefactorings(Document issue) {
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
                    System.out
                            .println("Refactorings for " + repoName + " at PR#" + prNumber + " Commit ID:" + commitId);
                    commitWithError[0] = commitId; // Assign the current commit ID
                    for (Refactoring ref : refactorings) {
                        String type = "";
                        String filePath = "";
                        int startLine = 0;
                        int endLine = 0;
                        String codeElement = "";
                        String codeElementType = "";
                        String desc = "";

                        JSONObject refactoringObj = new JSONObject(ref.toJSON());
			            type = refactoringObj.getString("type");

                        System.out.println("refactoring name : " + type);

			            JSONArray refactoringProps = refactoringObj.getJSONArray("rightSideLocations");

                        for (JSONObject prop : refactoringProps){
                            filePath = prop.getString("filePath");
                            startLine = prop.getInt("startLine");
                            endLine = prop.getInt("endLine");
                            codeElement = prop.getString("codeElement");
                            codeElementType = prop.getString("codeElementType");
                            desc = prop.getString("description");

                            Document data = Document.parse(ref.toJSON()).append("commit_id",
                                commitId).append("repo_name", repoName).append("repo_fullname", repoFullName)
                                .append("pr_number", prNumber).append("file_path", filePath).append("start_line", startLine).append("end_line", endLine).append("code_element", codeElement).append("code_element_type", codeElementType).append("description", desc).append("perf_keyword", perfKeyword).append("bug_keyword", bugKeyword)
                                .append("issue_number", issueNumber).append("issue_title", issueTitle);
                                db.persistToDB("perf-refactorings", data);
                        }
                        // System.out.println(ref.toString());
                        // Document data = Document.parse(ref.toJSON()).append("commit_id",
                        //         commitId).append("repo_name", repoName).append("repo_fullname", repoFullName)
                        //         .append("pr_number", prNumber)
                        //         .append("perf_keyword", perfKeyword).append("bug_keyword", bugKeyword)
                        //         .append("issue_number", issueNumber).append("issue_title", issueTitle);
                        // db.persistToDB("perf-refactorings", data);
                    }
                }
            }, 100);
        } catch (Exception e) {
            // Log the commit ID causing the exception to a file
            logCommitErrorToFile(commitWithError[0], (String) repoName);
            System.out.println(
                    "An error occurred during the collection of refactorings for commit: " + commitWithError[0]);
            System.out.println("Error message: " + e.getMessage());
            e.printStackTrace(); // Print stack trace for debugging
        }
    }

    // public void getAllRefactorings(Repository repo, String projectName, String
    // branch,
    // MongoCollection<Document> collection) {
    // // final List<Document> refactoringDocs = new ArrayList<>();
    // final String project = projectName;
    // final String[] commitWithError = { null }; // Using a final array to hold the
    // commit ID
    // final MongoCollection<Document> dbCollection = collection;
    // try {
    // miner.detectAll(repo, branch, new RefactoringHandler() {
    // @Override
    // public void handle(String commitId, List<Refactoring> refactorings) {
    // System.out.println("Refactorings at " + commitId);
    // commitWithError[0] = commitId; // Assign the current commit ID to the array
    // try {
    // for (Refactoring ref : refactorings) {
    // Document doc = Document.parse(ref.toJSON()).append("project",
    // project).append("commitId",
    // commitId);
    // // refactoringDocs.add(doc);
    // // sendRefactoringsToDB(dbCollection, doc);
    // }
    // } catch (Exception e) {
    // System.out.println("An error occurred when collecting refactoring at commit:
    // " + commitId);
    // e.printStackTrace(); // Print stack trace for debugging
    // }
    // }
    // });
    // } catch (Exception e) {
    // // Log the commit ID causing the exception to a file
    // logCommitErrorToFile(commitWithError[0], projectName);
    // System.out.println(
    // "An error occurred during the collection of refactorings for commit: " +
    // commitWithError[0]);
    // System.out.println("Error message: " + e.getMessage());
    // e.printStackTrace(); // Print stack trace for debugging
    // }
    // }

    private void logCommitErrorToFile(String commitId, String projectName) {
        try (FileWriter writer = new FileWriter("refactorings_collection/logs/error.log", true)) {
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
