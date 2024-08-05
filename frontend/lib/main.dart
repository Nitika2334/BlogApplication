import 'package:flutter/material.dart';
import 'package:frontend/controllers/signupController.dart';
import 'package:frontend/screens/login_page.dart';
import 'package:frontend/screens/signup_page.dart';
import 'package:frontend/controllers/loginController.dart';
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

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Home Page'),
      ),
      body: Center(
        child: Text('Welcome to Home Page'),
      ),
    );
  }
}