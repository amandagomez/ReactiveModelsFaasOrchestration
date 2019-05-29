/*
    Workflow structure with the set of stages and their triggering events
 */
import java.util.HashMap;

public class Workflow {
    private String id;
    private HashMap<String, Stage> stages;      //The Key is the event/trigger and the Value contains information on the execution

    public static String invoke_trigger = "invoke";

    public Workflow(String id) {
        this.id = id;
        this.stages = new HashMap<>();
    }

    public String addStage(String trigger, Stage newStage){
        if (stages.isEmpty()) trigger = id + "_" + invoke_trigger;
        stages.put(trigger, newStage);
        return this.id + "_" + newStage.getId();    // To be used as trigger for next stages
    }

    public Stage getStage(String trigger){
        if (!stages.containsKey(trigger))
            System.out.println("The trigger provided is not linked to a Stage");
        return stages.get(trigger);
    }

    public String getId() {
        return id;
    }

    public HashMap<String, Stage> getStages() {
        return stages;
    }

}
