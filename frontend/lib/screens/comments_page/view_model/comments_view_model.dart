import 'package:flutter/material.dart';

import '../models/comments_model.dart';

class CommentsViewModel extends ChangeNotifier {
  final List<Comment> _comments = [
    Comment(
      author: 'John Doe',
      text: 'This is a great post!',
      timestamp: DateTime.now().subtract(const Duration(days: 2)),
    ),
    Comment(
      author: 'Jane Smith',
      text: 'I agree, very informative.',
      timestamp: DateTime.now().subtract(const Duration(days: 1)),
    ),
  ];

  List<Comment> get comments => _comments;

  void addComment(String author, String text) {
    final newComment = Comment(
      author: author,
      text: text,
      timestamp: DateTime.now(),
    );
    _comments.add(newComment);
    notifyListeners();
  }
}
