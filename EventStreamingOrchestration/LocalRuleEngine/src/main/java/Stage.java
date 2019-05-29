/*
    Stages structure as components of the Workflow
 */
public class Stage {
    private String id;
    private Long parallelism;
    private String action;

        public Stage(String id, Long parallelism, String action) {
        this.id = id;
        this.parallelism = parallelism;
        this.action = action;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public Long getParallelism() {
        return parallelism;
    }

    public void setParallelism(Long parallelism) {
        this.parallelism = parallelism;
    }

    public String getAction() {
        return action;
    }

    public void setAction(String action) {
        this.action = action;
    }

    @Override
    public String toString() {
        return "Stage{" +
                "id='" + id + '\'' +
                ", parallelism=" + parallelism +
                ", action='" + action + '\'' +
                '}';
    }
}
