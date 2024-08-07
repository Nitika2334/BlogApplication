import 'package:dio/dio.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../signup_model/newUser.dart';

class SignupController extends ChangeNotifier {
  TextEditingController username = TextEditingController();
  TextEditingController password = TextEditingController();
  TextEditingController email = TextEditingController();

  bool incorrectEmail = false;
  bool passwordError = false;

  String _message = "";

  Future<void> submit(BuildContext context) async {

    incorrectEmail = false;
    passwordError = false;

    NewUser newUser = NewUser(username: username.text.trim(), password: password.text.trim(), email: email.text.trim());

    bool validateResult = validateUser(newUser);

    if (validateResult) {
      bool serverResponse = await authenticateUser(newUser);
      if (serverResponse) {
        print("Success");
        await showMessage(context: context, title: "Success", message: 'Account created successfully');
        GoRouter.of(context).go('/home');
      } else {
        print("Error: $_message");
        await showMessage(context: context, title: "Error", message: _message);
      }
    } else {
      print("Error: $_message");
    }

    notifyListeners();
  }


  bool validateUser(NewUser user) {
    if (user.username!.isEmpty || user.password!.isEmpty || user.email!.isEmpty) {
      _message = "Fields cannot be empty";
      return false;
    }

    if (user.password!.length < 8) {
      passwordError = true;
      _message = "Password must be at least 8 characters long";
      return false;
    }

    if (!_isValidEmail(user.email!)) {
      _message = "Please enter a valid email address";
      return false;
    }

    return true;
  }

  bool _isValidEmail(String email) {
    String emailPattern =
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$';
    RegExp regex = RegExp(emailPattern);
    if(!regex.hasMatch(email)){
      incorrectEmail = true;
    }
    return regex.hasMatch(email);
  }

  Future<bool> authenticateUser(NewUser user) async {
    Dio dio = Dio();
    String apiUrl = 'http://10.0.2.2:5000/api/v1/register';

    try {
      // Configure Dio to not throw on error status codes
      dio.options.validateStatus = (status) {
        return status! < 500;
      };

      Map<String, dynamic> requestData = {
        'username': user.username,
        'password': user.password,
        'email': user.email,
      };

      final response = await dio.post(apiUrl, data: requestData);
      final responseData = response.data;

      if (response.statusCode == 200 && responseData['status'] == true) {
        return true;
      } else if (response.statusCode == 400) {
        final errorCode = responseData['error_status']['error_code'];
        switch (errorCode) {
          case '40001':
            _message = 'Please provide name, email, and password.';
            break;
          case '40002':
            _message = 'User already exists.';
            break;
          default:
            _message = 'An error occurred. Please try again.';
        }
      } else {
        _message = 'Unexpected error. Please try again.';
      }
      return false;
    } catch (e) {
      print("Error: $e");
      _message = 'Network error. Please check your connection.';
      return false;
    }
  }




  Future<void> showMessage({required BuildContext context, required String title, required String message}) async {
    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: Text(title),
          content: Text(message),
          actions: [
            TextButton(
              child: const Text('Ok'),
              onPressed: () {
                Navigator.of(context).pop();
              },
            ),
          ],
        );
      },
    );
  }
}
