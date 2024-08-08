import 'dart:io';

class CreatePost {
  String? postTitle;
  String? postDescription;
  File? postImage;
  CreatePost({
    required this.postTitle,
    required this.postDescription,
    this.postImage,
  });
}
