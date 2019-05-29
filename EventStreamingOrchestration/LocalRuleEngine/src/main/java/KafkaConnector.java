/*
    Connector to the Condition Engine:
        - With Kafka service to publish Conditions
        - With Kafka Streams to subscribe for Orchestration events
 */

import avro.pojo.Execution;
import io.confluent.kafka.serializers.AbstractKafkaAvroSerDeConfig;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.apache.kafka.common.serialization.StringSerializer;

import java.io.FileInputStream;
import java.io.IOException;
import java.util.Collections;
import java.util.Properties;
import java.util.Set;

public class KafkaConnector {
    private String bootstrapServers;
    private String schemaRegistryUrl;
    private String executionCompletionT;
    private String executionInfoT;

    public KafkaConnector() {
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
        this.bootstrapServers = prop.getProperty("bootstrap_servers");
        this.schemaRegistryUrl = prop.getProperty("schema_registry_url");
        this.executionCompletionT = prop.getProperty("topic_finalization_events");
        this.executionInfoT = prop.getProperty("topic_conditions");
    }

    /*
        Publish the workflows' Conditions to Kafka service
     */
    public void setupKafka(Workflow wf){

        final Properties producerConfig = new Properties();
        producerConfig.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        producerConfig.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        producerConfig.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, io.confluent.kafka.serializers.KafkaAvroSerializer.class);
        producerConfig.put(AbstractKafkaAvroSerDeConfig.SCHEMA_REGISTRY_URL_CONFIG, schemaRegistryUrl);
        final KafkaProducer<String, Execution> producer = new KafkaProducer<>(producerConfig);

        Set<String> keys = wf.getStages().keySet();
        for(String key: keys){
            Stage stageAux = wf.getStage(key);
            Execution execAux = new Execution(wf.getId() + "_" + stageAux.getId(), stageAux.getParallelism());
            producer.send(new ProducerRecord<>(executionInfoT, execAux.getId(), execAux));
        }
        producer.flush();
        producer.close();
    }


    /*
        Subscribe to Kafka Streams to receive Orchestration events
     */
    public KafkaConsumer subscribeKafka(){

        final Properties consumerProperties = new Properties();
        consumerProperties.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        consumerProperties.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
        consumerProperties.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG,  StringDeserializer.class);
        consumerProperties.put(AbstractKafkaAvroSerDeConfig.SCHEMA_REGISTRY_URL_CONFIG, schemaRegistryUrl);
        consumerProperties.put(ConsumerConfig.GROUP_ID_CONFIG, "completion-events-consumer");
        final KafkaConsumer<String, Execution> consumer = new KafkaConsumer<>(consumerProperties);

        consumer.subscribe(Collections.singleton(executionCompletionT));

        return consumer;
    }
}
