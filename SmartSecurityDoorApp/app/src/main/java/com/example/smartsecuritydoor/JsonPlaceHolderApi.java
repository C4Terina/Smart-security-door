package com.example.smartsecuritydoor;

import java.util.List;

import retrofit2.Call;
import retrofit2.http.GET;

public interface JsonPlaceHolderApi {

    @GET("data")
    Call<List<Post>> getPost();


}
