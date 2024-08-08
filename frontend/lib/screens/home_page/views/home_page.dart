import 'package:flutter/material.dart';
import 'package:frontend/screens/create_post_page/views/create_post_view.dart';
import 'package:frontend/screens/edit_post_page/views/edit_view.dart';
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
      body: _currentIndex == 0 ? _pages[0] : _pages[1],
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentIndex,
        onTap: (index) {
          if (index == 1) {
            // Navigate to CreatePostView when the "Create" tab is tapped
            Navigator.push(
              context,
              MaterialPageRoute(builder: (context) => CreatePostView()),
            );
          } else if (index == 2) {
            // Navigate to EditView when the "Edit" tab is tapped
            Navigator.push(
              context,
              MaterialPageRoute(builder: (context) => EditView()),
            );
          } else {
            setState(() {
              _currentIndex = index;
            });
          }
        },
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.home),
            label: 'Home',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.create_new_folder_outlined),
            label: 'Create',
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
