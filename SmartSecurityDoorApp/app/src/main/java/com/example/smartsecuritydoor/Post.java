package com.example.smartsecuritydoor;

public class Post {


    private int entry_id;
    private int camera_id;
    private int person_id;
    private String person_name;
    private String time_recognised;

    public Post(int entry_id, int camera_id, String person_name, String time_recognised) {
        this.entry_id = entry_id;
        this.camera_id = camera_id;
        this.person_name = person_name;
        this.time_recognised = time_recognised;
    }

    public int getEntry_id() {
        return entry_id;
    }

    public void setEntry_id(int entry_id) {
        this.entry_id = entry_id;
    }

    public int getCamera_id() {
        return camera_id;
    }

    public void setCamera_id(int camera_id) {
        this.camera_id = camera_id;
    }

    public int getPerson_id() {
        return person_id;
    }

    public void setPerson_id(int person_id) {
        this.person_id = person_id;
    }

    public String getPerson_name() {
        return person_name;
    }

    public void setPerson_name(String person_name) {
        this.person_name = person_name;
    }

    public String getTime_recognised() {
        return time_recognised;
    }

    public void setTime_recognised(String time_recognised) {
        this.time_recognised = time_recognised;
    }
}
