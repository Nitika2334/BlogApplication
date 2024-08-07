// viewmodels/post_viewmodel.dart
import 'package:flutter/material.dart';

import '../models/home_model.dart';

class PostViewModel with ChangeNotifier {
  List<Post> _posts = [
    Post(title: "Post 1", content: "Content of post 1"),
    Post(title: "Post 2", content: "Content of post 2"),
  ];

  List<Post> get posts => _posts;

  void addPost(Post post) {
    _posts.add(post);
    notifyListeners();
  }
}
