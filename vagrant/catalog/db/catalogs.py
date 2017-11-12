# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Catalog, Item


engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
session = sessionmaker(bind=engine)()

Animals = Catalog(name="Animals")
session.add(Animals)
session.commit()

Company = Catalog(name="Company")
session.add(Company)
session.commit()

Food = Catalog(name="Food")
session.add(Food)
session.commit()

Sports = Catalog(name="Sports")
session.add(Sports)
session.commit()


# Company Items
Amazon = Item(
	name="Amazon",
	description="Amazon.com, Inc., doing business as Amazon, is an American electronic commerce and cloud computing company based in Seattle, Washington that was founded by Jeff Bezos on July 5, 1994.",
	catalog=Company
)
session.add(Amazon)
session.commit()

Facebook = Item(
	name="Facebook",
	description="Facebook is an American for-profit corporation and an online social media and social networking service based in Menlo Park, California. The Facebook website was launched on February 4, 2004, by Mark Zuckerberg, along with fellow Harvard College students and roommates, Eduardo Saverin, Andrew McCollum, Dustin Moskovitz, and Chris Hughes",
	catalog=Company
)
session.add(Facebook)
session.commit()

Google = Item(
	name="Google",
	description="Google LLC is an American multinational technology company that specializes in Internet-related services and products. These include online advertising technologies, search, cloud computing, software, and hardware. Google was founded in 1998 by Larry Page and Sergey Brin while they were Ph.D. students at Stanford University, in California",
	catalog=Company
)
session.add(Google)
session.commit()

Twitter = Item(
	name="Twitter",
	description="Twitter is an online news and social networking service where users post and interact with messages, \"tweets\", restricted to 140 characters. Registered users can post tweets, but those who are unregistered can only read them. Users access Twitter through its website interface, SMS or a mobile device app. Twitter, Inc. is based in San Francisco, California, United States, and has more than 25 offices around the world",
	catalog=Company
)
session.add(Twitter)
session.commit()

Udacity = Item(
	name="Udacity",
	description="Udacity is a for-profit educational organization founded by Sebastian Thrun, David Stavens, and Mike Sokolsky offering massive open online courses (MOOCs). According to Thrun, the origin of the name Udacity comes from the company's desire to be \"audacious for you, the student\". While it originally focused on offering university-style courses, it now focuses more on vocational courses for professionals.",
	catalog=Company
)

session.add(Udacity)
session.commit()

# Sports Items
Basketball = Item(
	name="Basketball",
	description="Basketball is a limited contact sport played on a rectangular court. While most often played as a team sport with five players on each side, three-on-three, two-on-two, and one-on-one competitions are also common. The objective is to shoot a ball through a hoop 18 inches (46 cm) in diameter and 10 feet (3.048 m) high that is mounted to a backboard at each end of the court. The game was invented in 1891 by Dr. James Naismith",
	catalog=Sports
)
session.add(Basketball)
session.commit()

Football = Item(
	name="Football",
	description="Football is a family of team sports that involve, to varying degrees, kicking a ball with the foot to score a goal. Unqualified, the word football is understood to refer to whichever form of football is the most popular in the regional context in which the word appears. Sports commonly called 'football' in certain places include: association football (known as soccer in some countries); gridiron football (specifically American football or Canadian football); Australian rules football; rugby football (either rugby league or rugby union); and Gaelic football. These different variations of football are known as football codes",
	catalog=Sports
)
session.add(Football)
session.commit()

Swimming = Item(
	name="Swimming",
	description="Swimming is an individual or team sport that uses arms and legs to move the body through water. The sport takes place in pools or open water (e.g., in a sea or lake). Competitive swimming is one of the most popular Olympic sports.", 
	catalog=Sports
)
session.add(Swimming)
session.commit()
