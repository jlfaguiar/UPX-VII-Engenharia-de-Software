import { createUserWithEmailAndPassword } from "firebase/auth";
import React, {useState} from "react";
import { View, Text, Image, StyleSheet, TextInput,  TouchableOpacity} from "react-native";
import { auth } from "../../Services/firebaseConfig";
import { collection, addDoc } from 'firebase/firestore';
import { db } from "../../Services/firebaseConfig";

export const Register = () => {

  const [email, setEmail] = useState("");
  const [nome, setNome] = useState("");
  const [telefone, setTelefone] = useState("");
  const [RA, setRA] = useState("");
  const [senha, setSenha] = useState("");
  const [confSenha, setConfSenha] = useState("");
  // Usar para autenticação posteriormente, cadastramento de usuários

  function checkPassword() {
    if (senha != confSenha) {
      alert('Senhas divergentes!');
      return 1;
    }
    return 0;
  }
  
  function checkAllFields() {
    if (nome == null || nome == '') {
      alert('Preencha o campo nome!');
      return 1;
    } else if (email == null || email == '') {
      alert('Preencha o campo e-mail!');
      return 1;
    } else if (telefone == null || telefone == '') {
      alert('Preencha o campo telefone!');
      return 1;
    } else if (RA == null || RA == '') {
      alert('Preencha o campo RA!');
      return 1;
    } else if (isNaN(Number(String(RA)))) {
      alert('O campo de RA deve ser numérico!');
      return 1;
    } else if (senha == null || senha == '') {
      alert('Preencha o campo senha!');
      return 1;
    } else if (confSenha == null || confSenha == '') {
      alert('Preencha o campo de conferência de senha!');
      return 1;
    } else {
      return 0;
    }
  }

  function criarUser() {
    if (checkAllFields() == 1) {
      return;
    }

    if (checkPassword() == 1) {
      return
    }

    createUserWithEmailAndPassword(auth, email, senha)
      .then((userCredential) => {
        const user = userCredential.user;
        alert('Usuário cadastrado com sucesso!');
        addDoc(collection(db, 'users_passageiros'), {
          ra: RA,
          email: email,
          user_id: userCredential.user.uid,
          nome: nome,
          telefone: telefone
        })
      })
      .catch((error) => {
        const errorCode = error.code;
        const errorMessage = error.message;
        alert('Um erro desconhecido ocorreu ao registrar o usuário!\nCódigo: ' + errorCode + '\nDescrição: ' + errorMessage)
      })
  }

  return (
    <View style={registerStyles.container}>

      <View style={registerStyles.div}>
        <Text style={{
          color: '#5CC6BA',
          alignSelf: 'center',
          fontSize: 30,
        }}>
          Cadastro de Passageiro
        </Text>

        <View style={{ flex: 2 }} />

        <TextInput style={registerStyles.text_input} placeholder="Nome Completo" onChangeText={
          (field) => setNome(field)
        } />


        <TextInput style={registerStyles.text_input} placeholder="E-mail" onChangeText={
          (field) => setEmail(field)
        } />

        <TextInput style={registerStyles.text_input} placeholder="RA" onChangeText={
          (field) => setRA(field)
        } />

        <TextInput style={registerStyles.text_input} placeholder="Telefone" onChangeText={
          (field) => setTelefone(field)
        } />

        <TextInput style={registerStyles.text_input_password} placeholder="Senha" onChangeText={
          (field) => setSenha(field)
        } secureTextEntry={true} />

        <TextInput style={registerStyles.text_input_password} placeholder="Confirme sua Senha" onChangeText={
          (field) => setConfSenha(field)
        } secureTextEntry={true} />

        <View style={{ flex: 2 }} />

        <TouchableOpacity title='Cadastrar' onPress={() => { criarUser() }} style={registerStyles.button}>
          <Text style={registerStyles.button_text}>
            Cadastrar
          </Text>
        </TouchableOpacity>

        <View style={{ flex: 1 }} />

      </View>

    </View>
  );
};

const registerStyles = StyleSheet.create({
  register: {
    backgroundColor: "#ffffff",
    display: "flex",
    flexDirection: "row",
    justifyContent: "center",
    width: "100%",
  },

  div: {
    backgroundColor: "#ffffff",
    height: 640,
    position: "relative",
    width: 360,
  },

  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },

  text_input: {
    backgroundColor: "#d9d9d9",
    width: '80%',
    alignSelf: 'center',
    marginTop: 20,
    height: 40,
    borderRadius: 30,
    textAlign: 'center',
    fontSize: 20
  },

  text_input_password: {
    backgroundColor: "#d9d9d9",
    width: '80%',
    alignSelf: 'center',
    marginTop: 20,
    height: 40,
    borderRadius: 30,
    textAlign: 'center',
    fontSize: 20
  },

  button: {
    backgroundColor: "#5CC6BA",
    width: '80%',
    alignSelf: 'center',
    marginTop: 20,
    height: 40,
    borderRadius: 30,
    textAlign: 'center',
    fontSize: 20,
    alignItems: 'center',
    justifyContent: 'center'
  },

  button_text: {
    textAlign: 'center',
    fontSize: 20,
    color: 'white'
  }
});

export default registerStyles;
