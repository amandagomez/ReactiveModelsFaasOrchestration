/*
  Main application processing the stream of events
 */

package main.scala.KafkaStreamingApp

import java.util.{Collections, Properties}
import avro.pojo.Execution
import io.confluent.kafka.serializers.AbstractKafkaAvroSerDeConfig
import io.confluent.kafka.streams.serdes.avro.SpecificAvroSerde
import org.apache.kafka.common.serialization.Serde
import org.apache.kafka.streams.{KafkaStreams, StreamsConfig}
import org.apache.kafka.streams.scala.{Serdes, StreamsBuilder}
import org.apache.kafka.streams.scala.kstream.{KStream, KTable}
import org.apache.kafka.streams.scala.ImplicitConversions._

object StreamProcessor extends App {
  import Serdes._

  val bootstrapServers = if (args.length > 0) args(0)
  else "localhost:9092"
  val schemaRegistryUrl = if (args.length > 1) args(1)
  else "http://localhost:8081"

  // Create the Events stream
  val streams: KafkaStreams = buildEventsFeed(bootstrapServers, schemaRegistryUrl, "/tmp/kafka-streams")

  // Start streams app
  streams.cleanUp()
  streams.start()

  // Add shutdown hook to respond to SIGTERM and gracefully close Kafka Streams
  sys.ShutdownHookThread{
    streams.close()
  }

  def buildEventsFeed(bootstrapServers: String, schemaRegistryUrl: String, stateDir: String) : KafkaStreams = {

    // Configuration for the Stream
    val streamsConfiguration = new Properties
    // Give the Streams application a unique name.  The name must be unique in the Kafka cluster against which the application is run.
    streamsConfiguration.put(StreamsConfig.APPLICATION_ID_CONFIG, "stream-processor")
    streamsConfiguration.put(StreamsConfig.CLIENT_ID_CONFIG, "stream-processor-client")
    // Where to find Kafka broker(s).
    streamsConfiguration.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers)
    // Where to find the Confluent schema registry instance(s)
    streamsConfiguration.put(AbstractKafkaAvroSerDeConfig.SCHEMA_REGISTRY_URL_CONFIG, schemaRegistryUrl)
    // Where to save intermediate results
    streamsConfiguration.put(StreamsConfig.STATE_DIR_CONFIG, stateDir)
    // Exactly once processing of records and latency
    streamsConfiguration.put(StreamsConfig.PROCESSING_GUARANTEE_CONFIG, StreamsConfig.EXACTLY_ONCE)


    val builder = new StreamsBuilder

    // Create the AvroSerde for Execution class serialization and deserialization
    implicit val specificAvroSerde: Serde[Execution] = {
      val sas = new SpecificAvroSerde[Execution]
      val isKeySerde: Boolean = false
      sas.configure(Collections.singletonMap(AbstractKafkaAvroSerDeConfig.SCHEMA_REGISTRY_URL_CONFIG, schemaRegistryUrl), isKeySerde)
      sas
    }

    // Execution's data as Stream, stored as KTable for future processing
    //https://docs.confluent.io/current/streams/faq.html Convert a KStream to a KTable without an aggregation step
    val staging_stream: KStream[String, Execution] = builder.stream[String, Execution](TopicConfig.CONDITIONS_T)
    staging_stream.to(TopicConfig.STORED_CONDITIONS_T)
    val stages: KTable[String, Execution] = builder.table[String, Execution](TopicConfig.STORED_CONDITIONS_T)

    // Arrival of events (function Finalization) and per-key aggregation
    val donesStream: KStream[String, String] = builder.stream[String, String](TopicConfig.FINALIZATION_EVENTS_T)
    val aggregated: KStream[String, Long] = donesStream.groupByKey.count.toStream
    val outputs: KTable[String, String] = donesStream.groupByKey.reduce((aggValue, newValue) => aggValue + "$" + newValue)

    // Join KTable and KStream to determine if aggregation is complete (when KStream is updated)
    // Take into account: Topics that are joined need to be co-partitioned, i.e. same number of partitions
    val dones: KStream[String, Execution] = aggregated.join(stages)((aggregatedValue, stageInfo) => if (stageInfo.getParallelism - aggregatedValue == 0) stageInfo else null).filter((_, value) => value != null)

    // Send Orchestration event to topic along with the outputs received
    val result: KStream[String, String] = dones.join(outputs)((_, outputString) => outputString)
    result.to(TopicConfig.ORCHESTRATION_EVENTS_T)

    new KafkaStreams(builder.build, streamsConfiguration)
  }

}