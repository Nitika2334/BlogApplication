import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';


class DeleteView extends StatelessWidget {
  const DeleteView({super.key});

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        return ClipRRect(
          borderRadius: const BorderRadius.vertical(top: Radius.circular(20)),
          child: Container(
            width: constraints.maxWidth,
            constraints: const BoxConstraints(
              maxHeight: 360,
            ),
            color: Colors.blueGrey[50],
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              mainAxisSize: MainAxisSize.min,
              children: [
                SizedBox(height: 3),
                Image.asset(
                  'assets/images/warning.png',
                  height: 110,
                ),
                Text("Delete this post?", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 27),),


                SizedBox(height: 8,),
                Center(
                  child: Text(
                    "Are you sure you want to delete\nthis post?",
                    textAlign: TextAlign.center,
                    style: TextStyle(fontSize: 17),
                  ),
                ),

                SizedBox(height: 8,),

                TextButton(
                  onPressed: () {},
                  child: Container(
                    width: double.infinity,
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      color: Colors.blue.shade800,
                      border: Border.all(color: Colors.blue.shade200),
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: const Padding(
                      padding: EdgeInsets.fromLTRB(9, 0, 0, 0),
                      child:
                          Center(
                            child: Text(
                              'Yes',

                              style: TextStyle(fontSize: 18,color: Colors.white ,fontWeight: FontWeight.bold),
                            ),
                          ),
                    ),
                  ),
                ),

                TextButton(
                  onPressed: () {
                    context.pop();
                  },
                  child: Container(
                    width: double.infinity,
                    padding: const EdgeInsets.fromLTRB(0, 2, 0, 12),
                    child: const Padding(
                      padding: EdgeInsets.fromLTRB(9, 0, 0, 0),
                      child:
                      Center(
                        child: Text(
                          'No',
                          style: TextStyle(fontSize: 18,color: Colors.blue,),
                        ),
                      ),
                    ),
                  ),
                ),

              ],
            ),
          ),
        );
      },
    );
  }
}
