import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  String? username;
  String? accessToken;

  @override
  void initState() {
    super.initState();
    _loadUserData();
  }

  Future<void> _loadUserData() async {
    var prefs = await SharedPreferences.getInstance();
    setState(() {
      username = prefs.getString('username');
      accessToken = prefs.getString('access_token');
    });
    print('Loaded username: $username');
    print('Loaded access token: $accessToken');
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: PreferredSize(
          preferredSize: Size.fromHeight(75.0),
          child: AppBar(
            title: Padding(
              padding: const EdgeInsets.fromLTRB(10, 30, 20, 10),
              child: Column(
                children: [
                  Text(
                    'Hi, $username!',
                    style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 25),
                  ),
                ],
              ),
            ),
            backgroundColor: Colors.purple,
          ),
        ),
        body: Center(child: Text('Content here')),
      ),
    );
  }
}
