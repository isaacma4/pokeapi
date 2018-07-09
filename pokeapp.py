#! /usr/bin/python
######################################################
#
# Author: Isaac Ma
# Date Created: June 14th, 2018
# Latest Revision: Jun 25th, 2018
# Copyright 2018, Isaac Ma, All rights reserved.
#
# Description: An application that takes in any
# amount of Pokemon names (best just to compare two 
# though) and outputs the Pokemon with the best type 
# advantage (if no clear advantage, then base stats
# is used as the comparison) using the RESTful API 
# available on https://pokeapi.co/
#
######################################################

import argparse
import os
import sys
import requests
import json
from pokemon import Pokemon

Filename = os.path.basename(__file__)
PokeAPI = "http://pokeapi.co/api/v2/"
DoubleDamageAdvantagePoints = 2
HalfDamageFromAdvantagePoints = 1
NoDamageDoneFromAdvantagePoints = 2

def getFavouredPokemonBasedOnStats(pokemonList):
    """
    Gets the strongest Pokemon based on based
    stats in the list of Pokemon.
    
    Inputs: list of Pokemon
    
    Outputs: the Pokemon with the best base stats
    """
    totalStatsList = [0]*len(pokemonList)
    for i in range(len(totalStatsList)):
        for stat in pokemonList[i].getBaseStats():
            totalStatsList[i] += stat["value"]
    bestStats = max(totalStatsList)
    for i in range(len(totalStatsList)):
        if bestStats == totalStatsList[i]:
            return pokemonList[i].getName()

def getAdvantagePointsBasedOnDamageRelation(types,
    pokemonToCmp, points):
    """
    Gets the total amount of advantage points to be
    added, comparing the types of one Pokemon to 
    another.
    
    Inputs: list of Pokemon
    
    Outputs: the Pokemon with the best base stats
    """
    totalPoints = 0
    for type in types:
        if type in pokemonToCmp.getTypes():
            totalPoints += points
    return totalPoints

def getArgs():
    parser = argparse.ArgumentParser(description='Poke App')
    parser.add_argument('pokemonNames', metavar='POKEMON',
                    action='store', type=str, nargs='+',
                    help='the name of a pokemon to compare \
                    against')
    args = parser.parse_args()
    return args

def getDamageRelationsForTypes(types):
    """
    Returns a list of damage relation data for a
    Pokemon retrieved from the PokeAPI.
    
    Inputs: a JSON formatted string of types
    for a Pokemon
    
    Outputs: a list of damage relations for all
    types given
    """
    damageRelations = []
    for type in types:
        response = requests.post(PokeAPI + "type/" + \
            type["type"]["name"])
        jsonData = json.loads(response.text)
        damageRelations.append(jsonData["damage_relations"])
    return damageRelations

def getFavouredPokemonBasedOnType(pokemonList):
    """
    Gets the strongest Pokemon based on best type
    advantages (i.e. Fighting is strong against Normal).
    See https://www.eurogamer.net/articles/2018-01-15-pokemon-go-type-chart-effectiveness-weaknesses
    for more details.
    In the case of no clear advantage, all the Pokemon 
    equally favoured with regards to types are returned.
    
    Inputs: list of Pokemon
    
    Outputs: one or more Pokemon with the best type 
    advantages
    """
    totalAdvantagesList = [0]*len(pokemonList)
    for i in range(len(totalAdvantagesList)):
        for j in range (len(totalAdvantagesList)):
            if i == j:
                continue
            totalAdvantagesList[i] += \
                getAdvantagePointsBasedOnDamageRelation(
                    pokemonList[i].getDoubleDamageToTypes(),
                    pokemonList[j],
                    DoubleDamageAdvantagePoints)
            totalAdvantagesList[i] += \
                getAdvantagePointsBasedOnDamageRelation(
                    pokemonList[i].getHalfDamageFromTypes(),
                    pokemonList[j],
                    HalfDamageFromAdvantagePoints)
            totalAdvantagesList[i] += \
                getAdvantagePointsBasedOnDamageRelation(
                    pokemonList[i].getNoDamageFromTypes(),
                    pokemonList[j],
                    NoDamageDoneFromAdvantagePoints)
    bestAdvantageTotal = max(totalAdvantagesList)
    bestAdvantagesList = []
    for i in range(len(totalAdvantagesList)):
        if bestAdvantageTotal == totalAdvantagesList[i]:
            bestAdvantagesList.append(pokemonList[i])
    return bestAdvantagesList

def parseBaseStats(statsJson):
    """
    Returns a dictionary of base stat values for a
    Pokemon retrieved from the PokeAPI.
    
    Inputs: a JSON formatted string of base stat
    values for a Pokemon
    
    Outputs: a dictionary matching stat name to value
    """
    stats = []
    for item in statsJson:
        stats.append({'name': item["stat"]["name"],
            'value': item["base_stat"]})
    return stats
    
def parseTypes(typesJson):
    """
    Returns a list of types for a Pokemon retrieved
    from the PokeAPI.
    
    Inputs: a JSON formatted string of type names
    for a Pokemon
    
    Outputs: a list of type names associated with
    a Pokemon
    """
    types = []
    for item in typesJson:
        types.append(item["type"]["name"])
    return types

def main():
    args = getArgs()
    if args.pokemonNames == None:
        print("Incorrect amount of data provided, please " +
            "enter name(s) or id(s) of the Pokemon you wish " +
            "to compare.")
        return
    pokemonList = []
    for i in range(len(args.pokemonNames)):
        response = requests.post(PokeAPI + \
            "pokemon/" + args.pokemonNames[i].lower())
        jsonData = json.loads(response.text)
        try:
            name = jsonData["forms"][0]["name"]
        except:
            print("Invalid data entered. Please enter " +
            "valid name(s) or id(s) of the Pokemon you " +
            "wish to compare.")
            return
        typesObject = jsonData["types"]
        types = parseTypes(typesObject)
        damageRelations = \
            getDamageRelationsForTypes(typesObject)
        baseStats = parseBaseStats(jsonData["stats"])
        pokemon = Pokemon(name,
                          types,
                          damageRelations,
                          baseStats)
        pokemonList.append(pokemon)
    favouredPokemon = \
        getFavouredPokemonBasedOnType(pokemonList)
    if len(favouredPokemon) > 1:
        bestStatsPokemon = \
            getFavouredPokemonBasedOnStats(favouredPokemon)
        print(bestStatsPokemon)
    else:
        print(favouredPokemon[0].getName())

if __name__ == "__main__":
    main()