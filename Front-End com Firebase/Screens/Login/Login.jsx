import React, { useEffect, useState } from "react";
import { StyleSheet } from 'react-native';
import { View, Text, TextInput, TouchableOpacity } from "react-native";
import { browserLocalPersistence, signInWithEmailAndPassword } from 'firebase/auth';
import { auth } from "../../Services/firebaseConfig";
import { setPersistence } from "firebase/auth";




const loginStyles = StyleSheet.create({
  login: {
    backgroundColor: '#ffffff',
    display: 'flex',
    flexDirection: 'row',
    justifyContent: 'center',
    width: '100%',
  },
  'View': {
    backgroundColor: '#ffffff',
    height: 640,
    position: 'relative',
    width: 360,
  },
  'line': {
    height: 1,
    left: 0,
    objectFit: 'cover',
    position: 'absolute',
    top: 592,
    width: 360,
  },
  'overlap-group': {
    height: 46,
    left: 30,
    position: 'absolute',
    top: 267,
    width: 300,
  },
  'rectangle': {
    backgroundColor: '#d9d9d9',
    borderRadius: 31,
    height: 45,
    left: 0,
    position: 'absolute',
    top: 1,
    width: 300,
  },
  'text-wrapper': {
    color: 'black',
    fontFamily: 'Roboto',
    fontSize: 20,
    fontWeight: '400',
    height: 45,
    position: 'absolute',
    textAlign: 'center',
    top: 0,
    width: 300,
  },
  'overlap': {
    backgroundColor: '#1e22e8',
    height: 46,
    left: 30,
    position: 'absolute',
    top: 411,
    width: 300,
    borderRadius: 20,
    borderWidth: 5,
    borderColor: '#1e22e8'
  },
  'button': {
    backgroundColor: '#5CC6BA',
    borderRadius: 80,
    top: 411,
    width: 300,
    position: 'absolute',
    alignContent: 'center',
    alignItems: 'center',
    height: 46,
    left: 30,
    justifyContent: 'center',
    alignItems: 'center',
    alignContent: 'center'
  },

  'overlap-2': {
    height: 46,
    left: 30,
    position: 'absolute',
    top: 335,
    width: 300,
  },
  'text-cad': {
    color: '#a0a0a0',
    fontFamily: 'Roboto',
    fontSize: 14,
    position: 'absolute',
    textAlign: 'center',
    top: '85%',
    alignSelf: 'center'
  },
  'text-cad-passageiro': {
    color: '#a0a0a0',
    fontFamily: 'Roboto',
    fontSize: 14,
    position: 'absolute',
    top: '90%',
    alignSelf: 'center'
  },
  'text-cad-motorista': {
    color: '#a0a0a0',
    fontFamily: 'Roboto',
    fontSize: 14,
    position: 'absolute',
    top: '95%',
    alignSelf: 'center'
  },
  'container': {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});

export default loginStyles;

export const Login = (props) => {

  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  // Usar para autenticação posteriormente

  function userLogin(){

    setPersistence(auth, browserLocalPersistence);
    signInWithEmailAndPassword(auth, email, senha)
      .then((userCredential) => {
        const user = userCredential.user;
        user.getIdToken().then((token) => {
          localStorage.setItem('userToken', token)
        })
        props.navigation.navigate('screenMain');
        return true;
      })
      .catch((error) => {
        const errorCode = error.code;
        const errorMessage = error.message;
        alert(errorMessage + errorCode);
      });
      return false;
  }

  useEffect(() => {
  }, [])


  return (
    <View style={loginStyles.container}>
      <View style={loginStyles.View}>

        <Text style={{
          color: '#5CC6BA',
          alignSelf: 'center',
          fontSize: 30,
        }}>FACENS Caronas</Text>

        <View style={loginStyles["overlap-group"]}>
          <View style={loginStyles.rectangle}/>
          <TextInput style={loginStyles["text-wrapper"]} placeholder="E-mail" onChangeText={
            (field) => setEmail(field)
          }/>
        </View>

        <View style={{flexDirection: 'row', flex: 1, alignContent: 'center'}}>
          <TouchableOpacity title='Entrar' onPress= {() => {
              loginStatus = userLogin();
              if (loginStatus) {
                props.navigation.navigate('screenMain')}
            }} style={loginStyles["button"]}>
              <Text style={{fontSize: 20, textAlign:'auto', textAlignVertical: 'top', color: 'white'}}>Acessar</Text>
          </TouchableOpacity>
        </View>
        
        <View style={loginStyles["overlap-2"]}>
          <View style={loginStyles.rectangle}/>
          <TextInput style={loginStyles["text-wrapper"]} placeholder="Senha" onChangeText={
            (field) => setSenha(field)
          } secureTextEntry={true}/>


        </View>
        <Text  style={loginStyles["text-cad"]}>
          Não possuí conta? Cadastre-se!
        </Text>

        <Text onPress={() =>{props.navigation.navigate('screenRegister')}}
         style={loginStyles["text-cad-passageiro"]}>
          Cadastrar como Passageiro
        </Text>

        <Text onPress={() =>{props.navigation.navigate('screenRegisterMotorista')}}
         style={loginStyles["text-cad-motorista"]}>
          Cadastrar como Motorista
        </Text>
      </View>
    </View>
  );
};
