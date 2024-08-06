import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../models/user.dart';

class LoginController extends ChangeNotifier {
  TextEditingController username = TextEditingController();
  TextEditingController password = TextEditingController();

  bool passwordError = false;

  String _message = "";

  Future<void> submit(BuildContext context) async {

    passwordError = false;

    User user = User(username: username.text.trim(), password: password.text.trim());

    bool validateResult = validateUser(user);

    if (validateResult) {
      passwordError = false;
      bool serverResponse = await authenticateUser(user);
      if (serverResponse) {
        print("Success");
        await showMessage(context: context, title: "Success", message: 'Login Successful');
        GoRouter.of(context).go('/home');
      } else {
        passwordError = true;
        print("Error: Incorrect Username or password");
        await showMessage(context: context, title: "Error", message: "Incorrect Username or password");
      }
    } else {
      passwordError = true;
      print("Error: $_message");
    }
    notifyListeners();
  }

  bool validateUser(User user) {
    if (user.username?.isEmpty == true || user.password?.isEmpty == true) {
      _message = "Username or password cannot be empty";
      return false;
    }
    if (user.username.toString().isEmpty) {
      _message = "Username cannot be empty";
      return false;
    }

    if (user.password!.isEmpty) {
      _message = "Password cannot be empty";
      return false;
    }

    if (user.password!.length < 8) {
      _message = "Password must be at least 8 characters long";
      return false;
    }

    return true;
  }

  Future<bool> authenticateUser(User user) async {
    Dio dio = Dio();
    String apiUrl = 'http://10.0.2.2:5000/api/v1/login';

    try {
      Map<String, dynamic> requestData = {
        'username': user.username,
        'password': user.password,
      };

      final response = await dio.post(apiUrl, data: requestData);

      if (response.statusCode == 200) {
        return true;
      } else {
        return false;
      }
    } catch (e) {
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
