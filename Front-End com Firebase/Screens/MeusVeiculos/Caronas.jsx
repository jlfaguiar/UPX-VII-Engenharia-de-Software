import { React, useEffect, useState } from "react";
import { Text, View, Image, FlatList, ScrollView, TouchableOpacity, Modal, TextInput, Dimensions } from "react-native";
import { StyleSheet } from "react-native";
import { auth } from "../../Services/firebaseConfig";
import { getDocs, query, collection, where, doc, deleteDoc, getDoc, addDoc, updateDoc, Timestamp } from 'firebase/firestore'
import { db } from "../../Services/firebaseConfig";
// import DateTimePickerModal from 'react-native-modal-datetime-picker';
import DateTimePicker from '@react-native-community/datetimepicker';

const windowHeight  = Dimensions.get('window').height;

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

    const [embarqueIdaPickerVisible, setEmbarqueIdaPickerVisible] = useState(false);
    const [embarqueVoltaPickerVisible, setEmbarqueVoltaPickerVisible] = useState(false);

    const [userData, setUserData] = useState({});
    const [userMotorista, setUserMotorista] = useState(false);

    const [motoristasData, setMotoristasData] = useState({})
    const [caronas, setCaronas] = useState([]);

    const [alreadyHaveGroup, setAlreadyHaveGroup] = useState(false);


    // Instruções de inicialização
    useEffect(() => {
        getUserData();
        getMotoristasData();
        getGruposDeCaronaData();
    }, [])

    useEffect(() => {
        console.log('Dados de usuário coletados')
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
            console.log('Coletando dados das caronas...')
            const collectionData = query(collection(db, 'grupos_de_carona')); 

            const snapshot = await getDocs(collectionData);

            snapshot.forEach((doc) => {
                newCaronaData.push({
                    id: doc.id,
                    horario_embarque_ida: doc.data().horario_embarque_ida,
                    horario_embarque_volta: doc.data().horario_embarque_volta,
                    string_horario_embarque_ida: timeStampToStringHourMinute(doc.data().horario_embarque_ida),
                    string_horario_embarque_volta: timeStampToStringHourMinute(doc.data().horario_embarque_volta),
                    valor: doc.data().valor,
                    string_valor: valueToMoneyString(doc.data().valor),
                    id_motorista: doc.data().id_motorista,
                    localizacao: doc.data().localizacao,
                    localizacao_desembarque: doc.data().localizacao_desembarque,
                    localizacao_embarque: doc.data().localizacao_embarque
                })
            })
            setCaronas(newCaronaData);
        } catch (error) {
            console.log('Erro ao coletar informações dos grupos de carona')
        }
    }

    const getMotoristasData = async () => {
        newMotoristasData = {}

        try {
            console.log('Coletando informações dos motoristas...')

            const collectionData = query(collection(db, 'users_motoristas'));

            const snapshot = await getDocs(collectionData);

            snapshot.forEach((doc) => {
                newMotoristasData[String(doc.data().user_id)] = {
                    'nome': doc.data().nome,
                    'telefone': doc.data().telefone
                }
            })

            setMotoristasData(newMotoristasData);

        } catch (error) {
            console.log('Erro ao coletar informações dos motoristas')
        }
    }

    // Obtenção de dados do firebase
    const popAdd = () => {
        return (
            <Modal animationType="fade" visible={menuAddCarona} transparent={true}>
                <View style={modalStyles.modalScreen}>
                    <View style={{ flex: 1 }} />

                    <Text style={modalStyles.modalTitle}>Adicionar Grupo de Carona</Text>

                    <View style={{ flex: 1 }} />

                    <TextInput placeholder="Localização de Embarque" style={modalStyles.inputField} onChangeText={setAddingLocalizacaoEmbarque} />

                    <TextInput placeholder="Localização de Desembarque" style={modalStyles.inputField} onChangeText={setAddingLocalizacaoDesembarque} />

                    <TextInput placeholder="Horário de Embarque (ida)" style={modalStyles.inputField}
                        //onTouchStart={() => { setEmbarqueIdaPickerVisible(true) }}
                        onFocus={() => { setEmbarqueIdaPickerVisible(true) }}
                        value={addingHorarioEmbarqueIda}
                    />

                    <TextInput placeholder="Horário de Embarque (volta)" style={modalStyles.inputField}
                        onTouchEnd={() => { setEmbarqueVoltaPickerVisible(true) }}
                        // onFocus={() => { setEmbarqueVoltaPickerVisible(true) }}
                        value={addingHorarioEmbarqueVolta} />

                    <TextInput placeholder="Valor" style={modalStyles.inputField} onChangeText={setAddingValor} />

                    <View style={{ flex: 1 }} />

                    <TouchableOpacity style={modalStyles.addButton} onPress={createCarona}>
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
                <View style={{ flex: 5 }}>
                    <Text style={{fontSize: 20, marginTop: 10, marginBottom: 10, color: '#5CC6BA'}}>
                        {motoristasData[carona.id_motorista]['nome']}
                    </Text>
                    <Text>
                        Ida: {carona.string_horario_embarque_ida} / Volta: {carona.string_horario_embarque_volta}
                    </Text>
                    <Text>
                        Valor (R$): {carona.string_valor}
                    </Text>
                    <Text style={{marginBottom: 15}}>
                        Telefone: {motoristasData[carona.id_motorista]['telefone']}
                    </Text>
                </View>
                <View style={{ flex: 1 }}>
                    {/* <Text></Text>  futuramente será usado para abrir detalhes da carona*/}
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
// Estilizações