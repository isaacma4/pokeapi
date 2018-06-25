#! /usr/bin/python
######################################################
#
# Author: Isaac Ma
# Date Created: June 25th, 2018
# Latest Revision: N/A
# Copyright 2018, Isaac Ma, All rights reserved.
#
# Description: A class used for storing information
# regarding a Pokemon's name, types, damage relations
# (according to other types) and base stats.
#
######################################################

class Pokemon:
	"""
	A class that represents information regarding
	a Pokemon as it relates to the PokeAPI.

	Attributes:
		name: name of the Pokemon
		types: the types of the Pokemon
		damageRelations: the damage relations
		according to other types
		baseStats: the base stats of the Pokemon
	"""
	def __init__(self, 
				 name,
				 types,
				 damageRelations,
				 baseStats):
		self.__name = name
		self.__types = types
		self.__damageRelations = damageRelations
		self.__baseStats = baseStats
	
	def getName(self):
		"""
		A function that returns the name of the Pokemon.
		"""
		return self.__name

	def getTypes(self):
		"""
		A function that returns the types of the Pokemon.
		"""
		return self.__types

	def getDamageRelations(self):
		"""
		A function that returns the damage relations of the Pokemon.
		"""
		return self.__damageRelations

	def __getTypesFromDamageRelation(self, damageRelationKey):
		"""
		A private function that returns the types that fall under a
		particular damage relation for this Pokemon.
		"""	
		types = []
		for damageRelation in self.__damageRelations:
			for type in damageRelation[damageRelationKey]:
				types.append(type["name"])
		return types
		
	def getDoubleDamageToTypes(self):
		"""
		A function that returns types of a damage relation that the
		Pokemon does double damage.
		"""	
		return self.__getTypesFromDamageRelation("double_damage_to")
	
	def getHalfDamageFromTypes(self):
		"""
		A function that returns types of a damage relation that the
		Pokemon takes half damage from.
		"""	
		return self.__getTypesFromDamageRelation("half_damage_from")
	
	def getNoDamageFromTypes(self):
		"""
		A function that returns types of a damage relation that the
		Pokemon takes no damage from.
		"""	
		return self.__getTypesFromDamageRelation("no_damage_from")
	
	def getBaseStats(self):
		"""
		A function that returns the base stats of the Pokemon.
		"""
		return self.__baseStats