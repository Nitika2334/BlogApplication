import 'dart:io';
import 'package:dio/dio.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:image_picker/image_picker.dart';

class CreatePostController with ChangeNotifier {
  TextEditingController title = TextEditingController();
  TextEditingController description = TextEditingController();

  File? _image;
  final _picker = ImagePicker();
  File? get image => _image;
  bool _showSpinner = false;

  bool get showSpinner => _showSpinner;

  void _setShowSpinner(bool value) {
    _showSpinner = value;
    notifyListeners();
  }

  Future<void> pickImage() async {
    _setShowSpinner(true);
    final pickedFile = await _picker.pickImage(source: ImageSource.gallery, imageQuality: 80);

    if (pickedFile != null) {
      _image = File(pickedFile.path);
    } else {
      print('No image selected');
    }
    _setShowSpinner(false);
  }

  Future<void> uploadDetails(BuildContext context) async {
    if (title.text.isEmpty || description.text.isEmpty) {
      print('Title or description is empty');
      return;
    }

    Dio dio = Dio();
    _setShowSpinner(true);

    try {
      Map<String, dynamic> formDataMap = {
        "title": title.text,
        "description": description.text,
      };

      if (_image != null) {
        String fileName = _image!.path.split('/').last;
        formDataMap["file"] = await MultipartFile.fromFile(_image!.path, filename: fileName);
      }

      FormData formData = FormData.fromMap(formDataMap);

      Response response = await dio.post(
        "API endpoint here for post upload",
        data: formData,
      );

      if (response.statusCode == 200) {
        // Handle success response
        print('Post uploaded successfully');
      } else {
        // Handle other status codes
        print('Post upload failed with status: ${response.statusCode}');
      }
    } catch (e) {
      print('Error uploading post: $e');
    } finally {
      _setShowSpinner(false);
    }
  }

  void removeImage() {
    _image = null;
    notifyListeners();
  }

  @override
  void dispose() {
    title.dispose();
    description.dispose();
    super.dispose();
  }
}
