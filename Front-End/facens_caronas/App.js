import { StyleSheet, Text, View } from 'react-native';
import { Login } from './Screens/Login/Login';
import {Register} from './Screens/Register/Register'
import { RegisterMotorista } from './Screens/RegisterMotoristas/RegisterMotorista';
import { NavigationContainer, useNavigation } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { Main } from './Screens/Main/Main';
// import { auth } from './Services/firebaseConfig';
import { useEffect, useState } from 'react';
import { auth } from './Services/firebaseConfig';

const Stack = createNativeStackNavigator();

export default function App() {
  
  const [user, setUser] = useState(null);

  useEffect(() => {
    auth.onAuthStateChanged((loggingUser) => {
      setUser(loggingUser);
    })
    console.log('Status de usuario', user)
  }, [])

  useEffect(() => {
    if(user != null) {
      console.log('Usuario já logado ' + user.uid)
    }
  }, [user])

  return (
      <NavigationContainer>
        <Stack.Navigator initialRouteName= {(user == null) ? 'screenLogin' : 'screenMain'}>
          <Stack.Screen name='screenLogin' component={Login} options={{headerShown: false} }  />
          <Stack.Screen name='screenRegister' component={Register} options={{headerShown: false}}/>
          <Stack.Screen name='screenRegisterMotorista' component={RegisterMotorista} options={{headerShown: false}}/>
          <Stack.Screen name='screenMain' component={Main} options={{headerShown: false}} />
        </Stack.Navigator>
      </NavigationContainer>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
