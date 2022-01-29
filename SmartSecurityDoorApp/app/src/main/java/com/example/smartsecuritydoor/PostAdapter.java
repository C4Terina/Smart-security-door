package com.example.smartsecuritydoor;

import android.content.Context;
import android.util.AttributeSet;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.recyclerview.widget.RecyclerView;

import java.util.List;

public class PostAdapter extends RecyclerView.Adapter<PostAdapter.ViewHolder> {

    private Context context;
    List<Post> postList;
    public PostAdapter(Context context, List<Post> postList){
        this.context = context;
        this.postList = postList;
    }

    @NonNull
    @Override
    public PostAdapter.ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(context).inflate(R.layout.post_item, parent, false);

        return new PostAdapter.ViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull PostAdapter.ViewHolder holder, int position) {

        Post post = postList.get(position);
        holder.entryIdTextView.setText("ID: " + post.getEntry_id());
        holder.cameraIdTextView.setText("Camera ID: " + post.getCamera_id());
        holder.personNameTextView.setText("Person Name: " + post.getPerson_name());
        holder.timeRecognizedTextView.setText("Time Recognised: " + post.getTime_recognised());

    }

    @Override
    public int getItemCount() {
        return postList.size();
    }

    public class ViewHolder extends RecyclerView.ViewHolder{

        public TextView entryIdTextView;
        public TextView cameraIdTextView;
        public TextView personNameTextView;
        public TextView timeRecognizedTextView;


        public ViewHolder(@NonNull View itemView) {
            super(itemView);

            entryIdTextView = itemView.findViewById(R.id.entryIdTextView);
            cameraIdTextView = itemView.findViewById(R.id.cameraIdTextView);
            personNameTextView = itemView.findViewById(R.id.personNameTextView);
            timeRecognizedTextView = itemView.findViewById(R.id.timeRecognizedTextView);

        }
    }
}
