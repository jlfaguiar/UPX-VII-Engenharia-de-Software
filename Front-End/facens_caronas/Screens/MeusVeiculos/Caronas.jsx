import { React, useEffect, useState } from "react";
import { Text, View, Image, FlatList, ScrollView, TouchableOpacity, Modal, TextInput, Dimensions } from "react-native";
import { StyleSheet } from "react-native";
import { auth } from "../../Services/firebaseConfig";
import { getDocs, query, collection, where, doc, deleteDoc, getDoc, addDoc, updateDoc, Timestamp } from 'firebase/firestore'
import { db } from "../../Services/firebaseConfig";
// import DateTimePickerModal from 'react-native-modal-datetime-picker';
import DateTimePicker from '@react-native-community/datetimepicker';
import axios from "axios";
import back_ip from "../../back_ip";

export const Caronas = (props) => {


    // Controle de pop-ups / Modais
    const [menuAddCarona, setMenuAddCarona] = useState(false);
    // const [menuEditCarona, setMenuEditCarona] = useState(false);

    const [addingLocalizacaoEmbarque, setAddingLocalizacaoEmbarque] = useState(null);
    const [addingLocalizacaoDesembarque, setAddingLocalizacaoDesembarque] = useState(null);
    const [addingValor, setAddingValor] = useState(0);
    const [addingHorarioEmbarqueIda, setAddingHorarioEmbarqueIda]  = useState(null);
    const [realAddingHorarioEmbarqueIda, setRealAddingHorarioEmbarqueIda]  = useState(null);
    const [addingHorarioEmbarqueVolta, setAddingHorarioEmbarqueVolta]  = useState(null);
    const [realAddingHorarioEmbarqueVolta, setRealAddingHorarioEmbarqueVolta]  = useState(null);

    const [edittingCaronaId, setEdittingCaronaId] = useState('');

    const [embarqueIdaPickerVisible, setEmbarqueIdaPickerVisible] = useState(false);
    const [embarqueVoltaPickerVisible, setEmbarqueVoltaPickerVisible] = useState(false);

    const [userData, setUserData] = useState({});
    const [userMotorista, setUserMotorista] = useState(false);

    const [caronas, setCaronas] = useState([]);

    const [alreadyHaveGroup, setAlreadyHaveGroup] = useState(false);
    
    const [modoEdicao, setModoEdicao] = useState(false);


    // Instruções de inicialização
    useEffect(() => {
        getUserData();
    }, [])

    useEffect(() => {
        console.log('Dados de usuário coletados')
        getGruposDeCaronaData()
    }, [userData])
    // Instruções de inicialização

    useEffect(() => {
        console.log('Dados de carona coletados');
        checkAlreadyHaveGroup();
    }, [caronas])

    const checkAlreadyHaveGroup = () => {
        const my_id = String(auth.currentUser.uid);

        caronas.forEach((carona) => {
            if (carona.id_motorista == my_id) {
                setAlreadyHaveGroup(true);
            }
        })

    }

    const changeEmbarqueIdaTime = (event, selectedTime) => {
        const currentTime = selectedTime || new Date();
        setAddingHorarioEmbarqueIda(dateToString(currentTime))
        setRealAddingHorarioEmbarqueIda(currentTime)
        setEmbarqueIdaPickerVisible(false);
    }

    const changeEmbarqueVoltaTime = (event, selectedTime) => {
        const currentTime = selectedTime || new Date();

        setAddingHorarioEmbarqueVolta(dateToString(currentTime))
        setRealAddingHorarioEmbarqueVolta(currentTime)
        setEmbarqueVoltaPickerVisible(false);
    }

    const cleanModalData = () => {
        setAddingLocalizacaoEmbarque(null);
        setAddingLocalizacaoDesembarque(null);
        setAddingHorarioEmbarqueVolta(null);
        setAddingHorarioEmbarqueIda(null);
        setRealAddingHorarioEmbarqueVolta(null);
        setRealAddingHorarioEmbarqueIda(null);
        setAddingValor(0);
        setEmbarqueVoltaPickerVisible(false);
        setEmbarqueIdaPickerVisible(false);
    }

    // Obtenção de dados do firebase
    const getUserData = async() => {

        const newUserData = {}

        try {
            console.log('Coletando dados de usuário...')
            console.log(auth.currentUser.uid)
            const collectionData = query(collection(db, 'users_motoristas')
            , where('user_id', '==', auth.currentUser.uid));

            const snapshot = await getDocs(collectionData);

            if (snapshot.size == 0) {

                const collectionData = query(collection(db, 'users_passageiros')
                , where('user_id', '==', auth.currentUser.uid));

                const snapshot = await getDocs(collectionData);
                
                if (snapshot.size == 0) {
                    console.log('Informações sobre usuário não encontradas')
                    return;
                } 
                newUserData['motorista'] = false
                newUserData['nome'] = snapshot.docs[0].data().nome
                newUserData['ra'] = snapshot.docs[0].data().ra
                newUserData['email'] = snapshot.docs[0].data().email
                newUserData['telefone'] = snapshot.docs[0].data().telefone
                newUserData['user_id'] = snapshot.docs[0].data().user_id
                newUserData['cnh'] = null
            } else {
                newUserData['motorista'] = true
                newUserData['nome'] = snapshot.docs[0].data().nome
                newUserData['ra'] = snapshot.docs[0].data().ra
                newUserData['email'] = snapshot.docs[0].data().email
                newUserData['telefone'] = snapshot.docs[0].data().telefone
                newUserData['user_id'] = snapshot.docs[0].data().user_id
                newUserData['cnh'] = snapshot.docs[0].data().cnh
            }

            setUserMotorista(newUserData['motorista'])
            setUserData(newUserData)

        } catch (error) {
            console.log('Erro ao coletar dados de usuário');
        }
    }

    const getGruposDeCaronaData = async() => {
        const newCaronaData = []
        try {
            console.log('Coletando dados das caronas....')

            const url_get = "http://" + back_ip + ":8000/api/grupodecarona/" + String(auth.currentUser.uid) + "/lista"
            console.log(url_get)
            const carona_snapshot = await axios.get(url_get);
           // const carona_snapshot = fetch(url_get)
            console.log('pegou!!!!')
            console.log(carona_snapshot)
            console.log('printou')

            carona_snapshot.data.forEach((doc) => {

                gp_carona = {
                    id: doc.id,
                    horario_embarque_ida: doc.horario_embarque_ida,
                    horario_embarque_volta: doc.horario_embarque_volta,
                    string_horario_embarque_ida: doc.horario_embarque_ida,
                    string_horario_embarque_volta: doc.horario_embarque_volta,
                    valor: doc.valor,
                    string_valor: valueToMoneyString(doc.valor),
                    localizacao: doc.localizacao,
                    localizacao_desembarque: doc.localizacao_desembarque,
                    localizacao_embarque: doc.localizacao_embarque,
                    total_passageiros: doc.total_passageiros,
                    max_passageiros: 4,
                    minha_carona: Boolean(doc.minha_carona),
                    nome_motorista: doc.nome_motorista,
                    telefone_motorista: doc.telefone_motorista,
                    carona_participante: doc.carona_participante
                }
                
                if (gp_carona.minha_carona) {
                    newCaronaData.unshift(gp_carona)
                } else {
                    newCaronaData.push(gp_carona)
                }

            })
            console.log('Estes sao os dados das caronas');
            console.log(newCaronaData);
            setCaronas(newCaronaData);
        } catch (error) {
            console.log(error)
            console.log('Erro ao coletar informações dos grupos de carona')
        }
    }


    const entrarEmGrupoDeCarona = async(id_grupo) => {

        grupo_obj = null;

        for (let carona of caronas) {
            if (String(carona.id) == id_grupo) {
                grupo_obj = carona;
                break;
            }
        }

        if (grupo_obj == null) {
            alert('Erro ao localizar informações do grupo de carona');
            return;
        } else if (grupo_obj.max_passageiros <= grupo_obj.total_passageiros) {
            alert('Este grupo de caronas já está no limite!');
            return;
        }

        console.log('Número de passageiros deste grupo: ' + String(grupo_obj.total_passageiros))
        
        const create_url = "http://" + back_ip + ":8000/api/associacaodecarona/novo"
        const body = {
            'id_passageiro': String(auth.currentUser.uid),
            'id_carona': grupo_obj.id
        }


        const create_response = await axios.post(create_url, body).then(() => {
            alert('Sucesso ao entrar no grupo de carona!');
            getGruposDeCaronaData()
        })
    }

    const sairDoGrupoDeCarona = async(id_grupo) => {

        const del_url = "http://" + back_ip + ":8000/api/associacaodecarona/" + String(auth.currentUser.uid) + "/" + String(id_grupo) + "/apagar"

        try {
            const delete_response = await axios.delete(del_url).then(() => {
            alert('Sucesso ao sair do grupo de carona!');
            getGruposDeCaronaData()
        })
           
        } catch (error) {
            console.log(error)
            console.log('Erro ao deletar associação em grupo de carona!');
        }

    }

    const abrirEditorDeCarona = (grupo) => {
        setAddingLocalizacaoEmbarque(grupo.localizacao_embarque);
        setAddingLocalizacaoDesembarque(grupo.localizacao_desembarque);
        setAddingHorarioEmbarqueVolta(grupo.string_horario_embarque_volta);
        setAddingHorarioEmbarqueIda(grupo.string_horario_embarque_volta);
        setRealAddingHorarioEmbarqueVolta(grupo.horario_embarque_volta);
        setRealAddingHorarioEmbarqueIda(grupo.horario_embarque_ida);
        setAddingValor(String(grupo.valor).replace('.', ','));
        setEmbarqueVoltaPickerVisible(false);
        setEmbarqueIdaPickerVisible(false);
        setEdittingCaronaId(grupo.id)
        setModoEdicao(true);
        setMenuAddCarona(true);

    }

    const editarGrupoDeCarona = async() => {
        console.log('vc quer editar entao kkkkkkkkkkkkkkkk')
    }


    // Obtenção de dados do firebase
    const popAdd = () => {
        return (
            <Modal animationType="fade" visible={menuAddCarona} transparent={true}>
                <View style={modalStyles.modalScreen}>
                    <View style={{ flex: 1 }} />

                    <Text style={modalStyles.modalTitle}>{modoEdicao ? 'Editar' : 'Adicionar'} Grupo de Carona</Text>

                    <View style={{ flex: 1 }} />

                    <TextInput placeholder="Localização de Embarque" style={modalStyles.inputField} onChangeText={setAddingLocalizacaoEmbarque} value={addingLocalizacaoEmbarque} />

                    <TextInput placeholder="Localização de Desembarque" style={modalStyles.inputField} onChangeText={setAddingLocalizacaoDesembarque} value={addingLocalizacaoDesembarque}/>

                    <TextInput placeholder="Horário de Embarque (ida)" style={modalStyles.inputField}
                        //onTouchStart={() => { setEmbarqueIdaPickerVisible(true) }}
                        onFocus={() => { setEmbarqueIdaPickerVisible(true) }}
                        value={addingHorarioEmbarqueIda}
                    />

                    <TextInput placeholder="Horário de Embarque (volta)" style={modalStyles.inputField}
                        onTouchEnd={() => { setEmbarqueVoltaPickerVisible(true) }}
                        // onFocus={() => { setEmbarqueVoltaPickerVisible(true) }}
                        value={addingHorarioEmbarqueVolta} />

                    <TextInput placeholder="Valor" style={modalStyles.inputField} onChangeText={setAddingValor} value={addingValor}/>

                    <View style={{ flex: 1 }} />

                    <TouchableOpacity style={modalStyles.addButton} onPress={modoEdicao ? editarGrupoDeCarona : createCarona}>
                        <Text style={modalStyles.buttonTextAdd}>Confirmar</Text>
                    </TouchableOpacity>

                    <TouchableOpacity style={modalStyles.cancelButton} onPress={() => {
                        setMenuAddCarona(false);
                        cleanModalData();
                    }}>
                        <Text style={modalStyles.buttonTextCancel}>Cancelar</Text>

                    </TouchableOpacity>

                    <View style={{ flex: 1 }} />
                </View>

                {embarqueIdaPickerVisible && (
                    <DateTimePicker
                        value={new Date()}
                        mode="time"
                        display="clock"
                        onChange={changeEmbarqueIdaTime}
                    />
                )}

                {embarqueVoltaPickerVisible && (
                    <DateTimePicker
                        value={new Date()}
                        mode="time"
                        display="clock"
                        onChange={changeEmbarqueVoltaTime}
                    />
                )}
            </Modal>
        )
    }

    const dateToString = (date_data) => {

        horas = date_data.getHours()
        minutos = date_data.getMinutes()

        horas = String(horas).padStart(2, '0')
        minutos = String(minutos).padStart(2, '0')

        return horas + ':' + minutos
    }

    const timeStampToStringHourMinute = (ts_data) => {

        ts_date = new Date(ts_data.seconds * 1000)
        
        string_hour_minute = dateToString(ts_date);

        return string_hour_minute
    }

    const valueToMoneyString = (num_data) => {

        const num_data_splitted = String(num_data).split('.')

        inteiros = num_data_splitted[0]

        centavos = '00'

        if (num_data_splitted.length > 1) {
            centavos = String(num_data_splitted[1]).padStart(2, '0')
        }

        if (centavos.length > 2) {
            centavos = centavos.slice(0, 2)
        }

        return (inteiros + ',' + centavos)
    } 

    const createCarona = () => {

        if (addingValor == 0 || addingLocalizacaoDesembarque == null || addingLocalizacaoDesembarque == null ||
            addingHorarioEmbarqueIda == null || addingHorarioEmbarqueVolta == null ||
            realAddingHorarioEmbarqueVolta == null || realAddingHorarioEmbarqueIda == null ) {
                alert('Preencha todos os campos para criar um grupo de caronas!');
                return;
         }


        if (isNaN(String(addingValor))) {
            alert('O valor da carona deve ser numérico!');
            return;
        }

        formated_horario_embarque_ida = new Timestamp(((new Date(realAddingHorarioEmbarqueIda)).getTime() / 1000), 0)
        formated_horario_embarque_volta = new Timestamp(((new Date(realAddingHorarioEmbarqueVolta)).getTime() / 1000), 0)


        addDoc(collection(db, 'grupos_de_carona'), {
           horario_embarque_ida: formated_horario_embarque_ida,
           horario_embarque_volta: formated_horario_embarque_volta,
           valor: Number(addingValor),
           localizacao_desembarque: addingLocalizacaoDesembarque,
           localizacao_embarque: addingLocalizacaoEmbarque,
           id_motorista: auth.currentUser.uid,
           localizacao: 'Campolim - Teste'
        }).then(() => {
            alert('Grupo de Carona Adicionado com Sucesso!');
            cleanModalData();
            setMenuAddCarona(false);
        })
    }

    const GrupoDeCarona = ({item}) => {

        carona = item

        return (
            <View style={{ backgroundColor: '#d9d9d9', flex: 1, borderRadius: 10, flexDirection: 'row' }}>
                <View style={{ flex: 2, alignItems: 'center', justifyContent: 'center', alignSelf: 'center'}}>
                    <Image  alt='driver_icon' source={require('./figs/driver_icon.png')} />
                </View>
                <View style={{ flex: 4 }}>
                    <Text style={{fontSize: 20, marginTop: 10, marginBottom: 10, color: '#5CC6BA'}}>
                        {carona.nome_motorista}
                    </Text>
                    <Text>
                        Ida: {carona.string_horario_embarque_ida} / Volta: {carona.string_horario_embarque_volta}
                    </Text>
                    <Text>
                        Valor (R$): {carona.string_valor}
                    </Text>
                    <Text>
                        Telefone: {carona.telefone_motorista}
                    </Text>
                    <Text style={{marginBottom: 15}}>
                        {carona.total_passageiros}/{carona.max_passageiros} Passageiros
                    </Text>
                </View>
                <View style={{ flex: 1, justifyContent: 'center' }}>
                    {/* <Text></Text>  futuramente será usado para abrir detalhes da carona*/}

                    {
                        item.minha_carona ? 
                        <Text style={GruposDeCaronasStyles.editButton} onPress={() =>
                            abrirEditorDeCarona(item)}> 
                            E
                        </Text> 
                        :
                        (!item.carona_participante ?
                        <Text style={GruposDeCaronasStyles.enterButton} onPress={() =>
                            entrarEmGrupoDeCarona(item.id)}> 
                            +
                        </Text> 
                        :
                        <Text style={GruposDeCaronasStyles.leaveButton} onPress={() =>
                            sairDoGrupoDeCarona(item.id)}>
                            X
                            </Text>)
                    }
                </View>
            </View>
        ) 
    }

    // Estrutura do componente principal
    return (
        <View style={{flex: 1, alignItems: 'center'}}>
            <Text style={listaGruposDeCaronasStyles.screenTitle}>Grupos de Caronas</Text>

            <ScrollView style={{flex: 10, width: '80%', height: '100%'}}>
                <FlatList data={caronas} renderItem={GrupoDeCarona} keyExtractor={item => item.id}
                ItemSeparatorComponent={<View style={{height: 15}} />}>

                </FlatList>
            </ScrollView>

            {popAdd()}

            {userMotorista && !alreadyHaveGroup ?
                <TouchableOpacity style={listaGruposDeCaronasStyles.addBox} onPress={() => { 
                    setMenuAddCarona(true)
                    }}>
                    <Image style={listaGruposDeCaronasStyles.addIcon} source={require('./imgs/addIcon.png')} />
                </TouchableOpacity>
                :
                <View />}
        </View>
    )
    // Estrutura do componente principal
}

// Estilizações
const listaGruposDeCaronasStyles = StyleSheet.create({
    screenTitle: {
        color: '#5CC6BA',
        fontSize: 25,
        marginTop: 70,
        marginBottom: 40
    },

    addBox: {
        backgroundColor: '#17d102',
        borderRadius: 30,
        height: 60,
        maxHeight: 60,
        position: 'relative',
        width: 60,
        maxWidth: 60,
        bottom: 25,
        flex: 1
    },
    addIcon: {
        height: 42,
        left: 9,
        position: "relative",
        top: 9,
        width: 42,
        alignContent: 'center',
    }
})


const modalStyles = StyleSheet.create({
    modalScreen: {
        backgroundColor: 'white',
        flexDirection: "column",
        justifyContent: "center",
        width: '100%',
        maxWidth: '100%',
        height: '100%',
        maxHeight: '100%',
        position: 'relative',
        alignSelf: 'center',
        alignItems: 'center',
        flex: 1
    },
    modalTitle: {
        color: '#5CC6BA',
        fontSize: 27,
        fontWeight: '700',
        left: 'center',
        letterSpacing: 0,
        position:'relative',
        width: 'auto',
        alignContent: 'center',
        alignSelf:'center',
        alignItems: 'center',
        justifyContent: 'center',
        marginBottom: 40,
        flex: 1
    },
    inputField : {
        color: 'black',
        fontFamily: 'Roboto',
        fontSize: 20,
        fontWeight: '400',
        height: "5%",
        position: 'relative',
        textAlign: 'left',
        top: 0,
        width: "80%",
        margin: 10,
        justifyContent: 'center',
        borderRadius: 50,
        backgroundColor: '#d9d9d9',
        paddingLeft: 15,
        flex: 1
    },
    cancelButton: {
        color: '#fc0303',
        backgroundColor: 'white',
        fontFamily: 'Roboto',
        fontSize: 20,
        fontWeight: '400',
        height: "5%",
        position: 'relative',
        textAlign: 'center',
        top: 0,
        width: "80%",
        margin: 10,
        justifyContent: 'center',
        borderColor: '#d9d9d9',
        borderWidth: 1,
        borderRadius: 15,
        alignItems: 'center',
        flex: 1,
    },
    addButton: {
        color: 'white',
        backgroundColor: '#5CC6BA',
        fontFamily: 'Roboto',
        fontSize: 20,
        fontWeight: '400',
        height: "5%",
        position: 'relative',
        textAlign: 'center',
        width: "80%",
        margin: 1,
        justifyContent: 'center',
        borderColor: 'black',
        borderWidth: 1,
        borderRadius: 15,
        alignItems: 'center',
        marginTop: 30,
        flex: 1,
    },
    buttonTextAdd: {
        fontSize: 20,
        fontFamily: 'Roboto',
        color: 'white',
        margin: 10

    },
    buttonTextCancel: {
        fontSize: 20,
        fontFamily: 'Roboto',
        color: '#5CC6BA'
    }
});

const GruposDeCaronasStyles = StyleSheet.create({
    enterButton: {
        borderRadius: 50, 
        backgroundColor: 'green',
        height: 40,
        width: 40,
        justifyContent: 'center',
        alignItems: 'center',
        textAlign: 'center',
        alignContent: 'center'
    },
    leaveButton: {
        borderRadius: 50, 
        backgroundColor: 'red',
        height: 40,
        width: 40,
        justifyContent: 'center',
        alignItems: 'center',
        textAlign: 'center',
        alignContent: 'center'
    },
    editButton: {
        borderRadius: 50, 
        backgroundColor: '#00d7fc',
        height: 40,
        width: 40,
        justifyContent: 'center',
        alignItems: 'center',
        textAlign: 'center',
        alignContent: 'center'
    }
})

// Estilizações

