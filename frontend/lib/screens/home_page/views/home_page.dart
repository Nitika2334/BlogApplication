import 'package:flutter/material.dart';
import 'package:frontend/screens/home_page/views/profile_view.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:frontend/screens/home_page/views/home_view.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: HomePage(),
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  int _currentIndex = 0;
  final List<Widget> _pages = [
    HomeView(),
    ProfileView(),
  ];

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
    return Scaffold(
      appBar: PreferredSize(
        preferredSize: Size.fromHeight(75.0),
        child: AppBar(
          title: Padding(
            padding: const EdgeInsets.fromLTRB(10, 30, 10, 10),
            child: Row(
              children: [
                Text(
                  'Hi, $username!',
                  style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 25),
                ),
                const Spacer(),
                const Icon(Icons.notifications_none_outlined, size: 30,),
              ],
            ),
          ),
          backgroundColor: Colors.white,
        ),
      ),
      body: _pages[_currentIndex],
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentIndex,
        onTap: (index) {
          setState(() {
            _currentIndex = index;
          });
        },
        items: [
          BottomNavigationBarItem(
            icon: Icon(Icons.home),
            label: 'Home',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.person),
            label: 'Profile',
          ),
        ],
      ),
    );
  }
}
