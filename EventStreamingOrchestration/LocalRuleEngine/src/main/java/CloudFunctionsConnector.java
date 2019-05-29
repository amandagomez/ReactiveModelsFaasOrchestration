/*
    Connector to IBM Cloud Functions to perform invocations
 */

import java.io.FileInputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Base64;
import java.util.Properties;

public class CloudFunctionsConnector {
    private String endpoint;
    private String namespace;
    private String api_key;
    private String auth;

    public CloudFunctionsConnector() {
        getConfig();
    }

    /*
        Get configuration from file
     */
    private void getConfig(){
        Properties prop = new Properties();
        try {
            String configPath = Thread.currentThread().getContextClassLoader().getResource("config.properties").getPath();
            prop.load(new FileInputStream(configPath));
        } catch (IOException e) {
            System.out.println("Could not retrieve config");
        }
        this.endpoint = prop.getProperty("endpoint");
        this.namespace = prop.getProperty("namespace");
        this.api_key = prop.getProperty("api_key");
        this.auth = Base64.getEncoder().encodeToString(this.api_key.getBytes());
    }

    /*
        Invoke deployed functions with payload
     */
    public void invokeFunction(String function_name, String id, String payload){
        try {
            // Generate URL
            String functionUrl = endpoint + "/api/v1/namespaces/" + namespace + "/actions/" + function_name;
            URL url = new URL(functionUrl);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();

            // Set Request Headers
            conn.setRequestProperty("Content-Type", "application/json");
            conn.setRequestProperty("Authorization", "Basic "+ auth);
            conn.setRequestMethod("POST");

            // Set Request Payload
            conn.setDoOutput(true);
            String input = "{\"id\": \"" + id + "\", \"input\": \"" + payload + "\"}";
            OutputStream os = conn.getOutputStream();
            os.write(input.getBytes());
            os.flush();
            os.close();

            // Request
            conn.getResponseCode();
            conn.disconnect();

        } catch (Exception e) {
            e.printStackTrace();
        }

    }
}
