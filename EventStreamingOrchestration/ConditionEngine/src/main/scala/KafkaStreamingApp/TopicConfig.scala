/*
  Kafka topics whose records need to be processed
 */

package main.scala.KafkaStreamingApp

object TopicConfig {
  private[KafkaStreamingApp] val CONDITIONS_T = "staging_topic"
  private[KafkaStreamingApp] val STORED_CONDITIONS_T = "intermediate_topic"
  private[KafkaStreamingApp] val FINALIZATION_EVENTS_T = "event_input_topic"
  private[KafkaStreamingApp] val ORCHESTRATION_EVENTS_T = "output_topic"
}
