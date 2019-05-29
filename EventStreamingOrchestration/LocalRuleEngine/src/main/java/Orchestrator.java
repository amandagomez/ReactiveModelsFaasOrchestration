/*
    The Orchestrator is the main class in charge of triggering and controlling the execution of a workflow.
        - Connected to Cloud Functions and the Condition Engine.
        - Contains a set of workflows and executes them.
 */
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;

import java.util.HashMap;
import java.util.List;
import java.util.Set;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class Orchestrator {
    private CloudFunctionsConnector cfConn;
    private KafkaConnector kfConn;
    private HashMap<String, Workflow> workflows;

    public Orchestrator() {
        cfConn = new CloudFunctionsConnector();
        kfConn = new KafkaConnector();
        workflows = new HashMap<>();
    }

    /*
        Add workflow to the Orchestrator set of workflows
     */
    public void addWorkflow(Workflow wf){
        if(workflows.containsKey(wf.getId())) System.out.println("Workflow with the ID specified already exists");
        else workflows.put(wf.getId(), wf);
    }

    /*
        Invoke a workflow and control its execution until termination
     */
    public void invokeWorkflow(String wfId, List<String> payload){
        Workflow current_wf = workflows.get(wfId);

        // Check if first stage can be launched (number of input elements VS parallelism of stage)
        if (payload.size() != current_wf.getStage(wfId + "_" + Workflow.invoke_trigger).getParallelism()) {
            System.out.println("Workflow not invoked, incorrect number of input elements");
            return;
        }

        // Send stages Conditions to Kafka through KafkaConnector
        kfConn.setupKafka(current_wf);

        // Launch first stage
        Stage firstStage = current_wf.getStage(wfId + "_" + Workflow.invoke_trigger);
        ExecutorService pool = Executors.newFixedThreadPool(firstStage.getParallelism().intValue());

        for (int i = 0; i < firstStage.getParallelism(); i++){
            String fPayload = payload.get(i);
            pool.execute(() -> cfConn.invokeFunction(firstStage.getAction(), wfId + "_" + firstStage.getId(), fPayload));
        }
        try {
            pool.shutdown();
            pool.awaitTermination(Long.MAX_VALUE, TimeUnit.SECONDS);
            System.out.println("Invoked workflow at \n" + System.currentTimeMillis());
        } catch (InterruptedException e) {
            e.printStackTrace();
            System.out.println("Received interruption while sample workflow");
            return;
        }

        // Subscribe to Orchestration events and launch new stages until the end of the workflow
        KafkaConsumer consumer = kfConn.subscribeKafka();
        Boolean wfEnded = false;
        while (!wfEnded) {
            final ConsumerRecords<String, String> consumerRecords = consumer.poll(100L);
            for (final ConsumerRecord<String, String> consumerRecord : consumerRecords) {
                System.out.println("Received " + consumerRecord.key() + "=" + consumerRecord.value());
                if (wfId.equals(consumerRecord.key().split("_")[0])){
                    // Look for stage in workflow and invoke
                    Stage invokeStage = workflows.get(wfId).getStage(consumerRecord.key());
                    if (invokeStage != null) {
                        System.out.println("Next invocation " + invokeStage.toString());
                        for (int i = 0; i < invokeStage.getParallelism(); i++)
                            cfConn.invokeFunction(invokeStage.getAction(), wfId + "_" + invokeStage.getId(), consumerRecord.value());
                    } else {
                        System.out.println("End of Workflow");
                        wfEnded = true;
                    }
                }
            }
        }
    }

    /*
        Testing
     */
    public void show_wf_testing(String wfId){
        Set<String> keys = workflows.get(wfId).getStages().keySet();
        for (String key: keys){
            System.out.println("trigger=" + key + " data= " + workflows.get(wfId).getStage(key));
        }
    }

}