package com.research;

public class ProjectsRegistry {
    public String[][] getProjects() {
        String[][] projects = {
                { "apm-agent", "./projects/apm-agent",
                        "https://github.com/elastic/apm-agent-java.git", "main" },
                { "jersey", "./projects/jersey",
                        "https://github.com/eclipse-ee4j/jersey.git", "2.x" },
                { "netty", "./projects/netty", "https://github.com/netty/netty.git", "main"
                },
                { "rdf4j", "./projects/rdf4j", "https://github.com/eclipse-rdf4j/rdf4j.git",
                        "main"
                },
                { "simpleflatmapper", "./projects/simpleflatmapper",
                        "https://github.com/arnaudroger/SimpleFlatMapper.git",
                        "master" },
                { "cantaloupe", "./projects/cantaloupe",
                        "https://github.com/cantaloupe-project/cantaloupe.git",
                        "develop" },
                { "debezium", "./projects/debezium",
                        "https://github.com/debezium/debezium.git", "main" },
                { "vert.x", "./projects/vert.x",
                        "https://github.com/eclipse-vertx/vert.x.git",
                        "master" },
                { "jctools", "./projects/jctools", "https://github.com/JCTools/JCTools.git",
                        "master" },
                { "jetty", "./projects/jetty", "https://github.com/jetty/jetty.project.git",
                        "jetty-12.0.x" },
                { "zipkin", "./projects/zipkin", "https://github.com/openzipkin/zipkin.git",
                        "master" },
        };

        return projects;
    }
}