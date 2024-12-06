import 'package:flutter/material.dart';
import 'package:frontend/screens/comments_page/view_model/comments_view_model.dart';
import 'package:frontend/screens/home_page/view_model/home_view_model.dart';
import 'package:frontend/screens/home_page/views/home_page.dart';

import 'package:frontend/screens/login_page/view_model/login_view_model.dart';
import 'package:frontend/screens/login_page/views/login_page.dart';
import 'package:frontend/screens/signup_page/viewmodel/signup_view_model.dart';
import 'package:frontend/screens/signup_page/views/signup_page.dart';
import 'package:provider/provider.dart';
import 'package:go_router/go_router.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => LoginController()),
        ChangeNotifierProvider(create: (_) => SignupController()),
        ChangeNotifierProvider(create: (_) => PostViewModel()),
        ChangeNotifierProvider(create: (context) => CommentsViewModel()),
      ],
      child: MaterialApp.router(
        title: 'Flutter Demo',
        routerConfig: _router,
        theme: ThemeData(
          colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
          useMaterial3: true,
        ),
      ),
    );
  }

  final GoRouter _router = GoRouter(
    initialLocation: "/login",
    routes: [
      GoRoute(
        path: "/home",
        builder: (context, state) => const HomePage(),
      ),
      GoRoute(
        path: "/login",
        builder: (context, state) => const LoginPage(),
      ),
      GoRoute(
        path: "/signup",
        builder: (context, state) => const SignupPage(),
      ),
    ],
  );
}

