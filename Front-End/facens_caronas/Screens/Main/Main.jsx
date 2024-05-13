import { React, useEffect } from "react";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { NavigationContainer, useNavigation } from "@react-navigation/native";
import { Image } from "react-native";
import { Caronas } from "../Caronas/Caronas";
import { StyleSheet } from "react-native";
import { auth } from "../../Services/firebaseConfig";

const Tab = createBottomTabNavigator();

export const Main = (props) => {

    const navigation = useNavigation();

    // Inicialização e verificação de estado
    useEffect(() =>{
        const unsubscribe = auth.onAuthStateChanged((user) => {
            if(!user) {
                navigation.navigate('screenLogin');
            }
        })

        return () => unsubscribe();
    }, [navigation])
    // Inicialização e verificação de estado

    // Estrutura do componente principal
    return (
        <NavigationContainer independent={true}>
            <Tab.Navigator screenOptions={{style: tabNavigationStyles.tabBar}}>

                <Tab.Screen name='minhasCaronasScreen' component={Caronas} options={{
                    tabBarLabel: '',
                    tabBarIcon: () => (
                        <Image source={require('./imgs/MeusVeiculosIcon.png')} style={tabNavigationStyles.icon}/>
                    ),
                    headerShown: false
                }} />

            </Tab.Navigator>
        </NavigationContainer>
    )
    // Estrutura do componente principal
}

// Estilizações
export const tabNavigationStyles = StyleSheet.create({
    tabBar: {
        borderTopWidth: 10,
        paddingHorizontal: 10,
        justifyContent: "space-between",
        flexDirection: 'row',
        paddingVertical: 5,
        alignItems: 'center',

    },
    icon: {
        top: 7,
        width: 30,
        height: 30
    }
})
// Estilizações