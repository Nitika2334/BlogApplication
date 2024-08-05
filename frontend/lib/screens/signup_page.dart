import 'package:flutter/material.dart';
import 'package:frontend/controllers/signupController.dart';
import 'package:get/get.dart';
import 'package:go_router/go_router.dart';
import 'package:provider/provider.dart';

import '../components/text_field.dart';


class SignupPage extends StatefulWidget {
  const SignupPage({super.key});

  @override
  State<SignupPage> createState() => _SignupPageState();
}

class _SignupPageState extends State<SignupPage> {

  SignupController controller = Get.put(SignupController());

  final emailController = TextEditingController();
  final usernameController = TextEditingController();
  final passwordController = TextEditingController();
  final confirmPassword = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[100],
      body: SafeArea(
        child: Center(
          child: Consumer<SignupController>(
            builder: (context, controller, child){
              return Column(
                children: [
                  const SizedBox(height: 40),
                  Image.asset(
                    'assets/images/appreciate_logo.png',
                    height: 130,
                  ),
                  const SizedBox(height: 3),
                  const Align(
                    alignment: Alignment.centerLeft,
                    child: Padding(
                      padding: EdgeInsets.fromLTRB(24, 20, 0, 20),
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.start,
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Let\'s go!',
                            style: TextStyle(fontSize: 30, fontWeight: FontWeight.bold),
                          ),
                          Text(
                            'Create a new account',
                            style: TextStyle(fontSize: 16),
                          ),
                        ],
                      ),
                    ),
                  ),

                  const SizedBox(height: 10,),


                  Expanded(
                    child: ListView(
                      padding: const EdgeInsets.symmetric(horizontal: 18.0, vertical: 0),
                      children: [

                        Padding(
                          padding: const EdgeInsets.fromLTRB(7,0,7,0),
                          child: Container(
                            width: double.infinity,
                            padding: const EdgeInsets.all(16),
                            decoration: BoxDecoration(
                              color: Colors.white,
                              borderRadius: BorderRadius.circular(25),
                              border: Border.all(
                                color: controller.incorrectEmail ? Colors.red : Colors.transparent,
                                width: 3,
                              ),
                            ),
                            child: Padding(
                              padding: const EdgeInsets.fromLTRB(9,0,0,0),
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    'Enter email id',
                                    style: TextStyle(fontSize: 18, color: Colors.grey.shade600),
                                  ),
                                  const SizedBox(height: 2),
                                  GenTextField(
                                    controller: controller.email,
                                    hintText: 'eg. johndoe@gmail.com',
                                    obscureText: false,
                                  ),

                                  if (controller.incorrectEmail)
                                    const Text(
                                      'Please enter valid email',
                                      style: TextStyle(color: Colors.red, fontSize: 17),
                                    ),
                                ],
                              ),
                            ),
                          ),
                        ),

                        const SizedBox(height: 26),

                        Padding(
                          padding: const EdgeInsets.fromLTRB(7,0,7,0),
                          child: Container(
                            width: double.infinity,
                            padding: const EdgeInsets.all(16),
                            decoration: BoxDecoration(
                              color: Colors.white,
                              borderRadius: BorderRadius.circular(25),
                            ),
                            child: Padding(
                              padding: const EdgeInsets.fromLTRB(9,0,0,0),
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    'Enter user name',
                                    style: TextStyle(fontSize: 18, color: Colors.grey.shade600),
                                  ),
                                  const SizedBox(height: 2),
                                  GenTextField(
                                    controller: controller.username,
                                    hintText: 'eg. John Doe',
                                    obscureText: false,
                                  ),
                                ],
                              ),
                            ),
                          ),
                        ),

                        const SizedBox(height: 26),

                        Padding(
                          padding: const EdgeInsets.fromLTRB(7,0,7,0),
                          child: Container(
                            width: double.infinity,
                            padding: const EdgeInsets.all(16),
                            decoration: BoxDecoration(
                              color: Colors.white,
                              borderRadius: BorderRadius.circular(25),
                            ),
                            child: Padding(
                              padding: const EdgeInsets.fromLTRB(9,0,0,0),
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                mainAxisAlignment: MainAxisAlignment.start,
                                children: [
                                  Text(
                                    'Enter password',
                                    style: TextStyle(fontSize: 18, color: Colors.grey.shade600),
                                  ),
                                  GenTextField(
                                    controller: controller.password,
                                    hintText: 'eg. password',
                                    obscureText: true,
                                  ),
                                ],
                              ),
                            ),
                          ),
                        ),


                        const SizedBox(height: 20),

                        Padding(
                          padding: const EdgeInsets.fromLTRB(9, 0, 9, 4),
                          child: SizedBox(

                            width: 100,
                            height: 50,
                            child: TextButton(
                              onPressed: () async {
                                await controller.submit(context);
                              },
                              style: TextButton.styleFrom(
                                foregroundColor: Colors.white,
                                backgroundColor: Colors.blue[700],
                                side: BorderSide.none,
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(10), // Set the border radius here
                                ),
                              ),
                              child: const Text('Sign up', style: TextStyle(fontSize: 15, ),),
                            ),
                          ),
                        ),
                        Row(
                          crossAxisAlignment: CrossAxisAlignment.center,
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            const Text('Already have an account?'),
                            TextButton(
                              onPressed: () {
                                context.go("/login");
                              },
                              style: TextButton.styleFrom(
                                padding: EdgeInsets.zero,
                                foregroundColor: Colors.blue[800],
                                backgroundColor: Colors.transparent,
                                side: BorderSide.none,
                              ),
                              child: const Text(
                                'Login',
                                style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold),
                              ),
                            ),
                          ],
                        )

                      ],
                    ),
                  ),
                ],
              );
            }
          )
        ),
      ),
    );
  }
}
