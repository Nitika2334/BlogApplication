import 'dart:io';

class EditPost{
  String? title;
  String? description;
  File? image;
  EditPost({required this.title, required this.description, this.image});
}