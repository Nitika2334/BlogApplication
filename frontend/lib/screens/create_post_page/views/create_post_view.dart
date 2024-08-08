import 'dart:io';
import 'package:flutter/material.dart';
import 'package:modal_progress_hud_nsn/modal_progress_hud_nsn.dart';
import 'package:provider/provider.dart';
import '../../../components/text_field.dart';
import '../view_model/create_view_model.dart';

class CreatePostView extends StatelessWidget {
  const CreatePostView({super.key});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider<CreatePostController>(
      create: (_) => CreatePostController(),
      child: Consumer<CreatePostController>(
        builder: (context, controller, child) {
          return ModalProgressHUD(
            inAsyncCall: controller.showSpinner,
            child: Scaffold(
              backgroundColor: Colors.grey.shade200,
              appBar: PreferredSize(
                preferredSize: const Size.fromHeight(80),
                child: AppBar(
                  title: const Text('Create post', style: TextStyle(fontWeight: FontWeight.bold)),
                ),
              ),
              body: SingleChildScrollView(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Align(
                      alignment: Alignment.centerLeft,
                      child: Padding(
                        padding: EdgeInsets.fromLTRB(24, 20, 0, 10),
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.start,
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              'Share your thoughts with the community',
                              style: TextStyle(fontSize: 16),
                            ),
                          ],
                        ),
                      ),
                    ),
                    const SizedBox(height: 10.0),
                    Padding(
                      padding: const EdgeInsets.fromLTRB(20, 0, 20, 0),
                      child: Container(
                        width: double.infinity,
                        padding: const EdgeInsets.all(15),
                        decoration: BoxDecoration(
                          color: Colors.white,
                          borderRadius: BorderRadius.circular(25),
                        ),
                        child: Padding(
                          padding: const EdgeInsets.fromLTRB(9, 0, 0, 0),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                'Title',
                                style: TextStyle(fontSize: 18, color: Colors.grey.shade600),
                              ),
                              const SizedBox(height: 2),
                              GenTextField(
                                controller: controller.title,
                                hintText: 'eg. Dive into the perfect',
                                obscureText: false,
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                    const SizedBox(height: 15),
                    Padding(
                      padding: const EdgeInsets.fromLTRB(20, 0, 20, 0),
                      child: Container(
                        width: double.infinity,
                        padding: const EdgeInsets.all(16),
                        decoration: BoxDecoration(
                          color: Colors.white,
                          borderRadius: BorderRadius.circular(25),
                        ),
                        child: Padding(
                          padding: const EdgeInsets.fromLTRB(9, 0, 0, 0),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                'Description',
                                style: TextStyle(fontSize: 18, color: Colors.grey.shade600),
                              ),
                              const SizedBox(height: 2),
                              GenTextField(
                                controller: controller.description,
                                hintText: 'eg. Dive into the perfect',
                                obscureText: false,
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                    const SizedBox(height: 20.0),
                    Padding(
                      padding: const EdgeInsets.fromLTRB(20, 0, 20, 0),
                      child: Container(
                        width: double.infinity,
                        padding: const EdgeInsets.all(16),
                        decoration: BoxDecoration(
                          color: Colors.white,
                          borderRadius: BorderRadius.circular(25),
                        ),
                        child: Padding(
                          padding: const EdgeInsets.fromLTRB(9, 0, 0, 0),
                          child: Row(
                            crossAxisAlignment: CrossAxisAlignment.center,
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Image.asset(
                                'assets/images/paper-clip.png',
                                width: 27,
                                height: 27,
                              ),
                              SizedBox(width: 7),
                              Text(
                                'Upload image',
                                style: TextStyle(fontSize: 18, color: Colors.grey.shade800),
                              ),
                              Spacer(),
                              TextButton(
                                onPressed: controller.pickImage,
                                style: TextButton.styleFrom(
                                  padding: EdgeInsets.zero,
                                  foregroundColor: Colors.blue[800],
                                  backgroundColor: Colors.transparent,
                                  side: BorderSide.none,
                                ),
                                child: const Text(
                                  'upload',
                                  style: TextStyle(
                                    fontSize: 15,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                    if (controller.image != null)
                      Padding(
                        padding: const EdgeInsets.all(20.0),
                        child: Image.file(
                          File(controller.image!.path),
                          height: 100.0,
                          width: 100.0,
                          fit: BoxFit.cover,
                        ),
                      ),
                    const SizedBox(height: 10.0),
                  ],
                ),
              ),
              bottomNavigationBar: Padding(
                padding: const EdgeInsets.fromLTRB(20, 0, 20, 30),
                child: SizedBox(
                  width: double.infinity,
                  height: 50,
                  child: TextButton(
                    onPressed: () async => controller.uploadDetails(context),
                    style: TextButton.styleFrom(
                      foregroundColor: Colors.white,
                      backgroundColor: Colors.blue[700],
                      side: BorderSide.none,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(10),
                      ),
                    ),
                    child: const Text(
                      'Create Post',
                      style: TextStyle(
                        fontSize: 15,
                      ),
                    ),
                  ),
                ),
              ),
            ),
          );
        },
      ),
    );
  }
}
