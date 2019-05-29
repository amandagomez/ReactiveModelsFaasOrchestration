/*
    Sample Workflow creation and invocation
 */
import java.util.Arrays;
import java.util.List;

public class sample {
    public static void main(String[] args) {

        long init = System.currentTimeMillis();

        Workflow wf0 = new Workflow("seq-00");
        String previous = "";

        // Parallel
        previous = wf0.addStage(previous, new Stage("st0", 10L, "wait5s"));

        // Sequence
        for (int i = 0; i < 2; i++){
            previous = wf0.addStage(previous, new Stage("st" + (i + 1), 1L, "wait5s"));
         }


        Orchestrator myO = new Orchestrator();
        myO.addWorkflow(wf0);
        List<String> input = Arrays.asList("a", "b", "c", "d", "e", "a", "b", "c", "d", "e");
        myO.invokeWorkflow(wf0.getId(), input);

        System.out.println(init);
        System.out.print(System.currentTimeMillis());
    }
}

