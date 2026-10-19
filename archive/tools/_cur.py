import json
P=lambda name,kind,role,title,key="photo",**kw: dict(name=name,kind=kind,role=role,_t={key:title},**kw)
cur={"svb":[
 P("Greg Becker","person","Former SVB CEO","File:Opening remarks by Greg Becker at Global Entrepreneurship Summit 2016 welcome reception.jpg"),
 P("Jerome Powell","person","Federal Reserve Chair","File:Jerome H. Powell, Federal Reserve Chair (cropped).jpg"),
 P("Janet Yellen","person","Treasury Secretary (2021-2025)","File:Secretary Janet Yellen portrait (cropped).jpg"),
 P("Martin Gruenberg","person","FDIC Chairman","File:Martin Gruenberg Portrait.jpg"),
 P("Michael S. Barr","person","Fed Vice Chair for Supervision","File:Michael S. Barr, Federal Reserve Member.jpg",aliases=["Michael Barr"]),
 P("Silicon Valley Bank","company","Startup bank, Santa Clara, Calif.","File:3003 West Tasman Drive entrance, Santa Clara, California.jpg","hq_photo",aliases=["SVB"]),
 P("Signature Bank","company","New York bank, failed Mar 12 2023","File:Signature bank storefront (39th & Madison).png","hq_photo"),
 P("First Citizens Bank","company","Acquired SVB deposits and loans","File:First Citizens Bank (50784933857).jpg","hq_photo",aliases=["First Citizens"]),
],"lehman":[
 P("Richard S. Fuld Jr.","person","Lehman CEO 1994-2008","File:Richard S. Fuld, Jr. at World Resources Institute forum (cropped).jpg",aliases=["Richard Fuld","Dick Fuld","Fuld"]),
 P("Henry Paulson","person","U.S. Treasury Secretary 2006-2009","File:Henry Paulson official Treasury photo, 2006 (cropped).jpg",aliases=["Hank Paulson","Paulson"]),
 P("Timothy Geithner","person","President, New York Fed (2008)","File:Timothy Geithner official portrait.jpg",aliases=["Geithner"]),
 P("Ben Bernanke","person","Federal Reserve Chair (2008)","File:Ben Bernanke official portrait (cropped).jpg",aliases=["Bernanke"]),
 P("Lehman Brothers Holdings Inc.","company","Fourth-largest U.S. investment bank","File:Lehman Brothers Times Square by David Shankbone.jpg","hq_photo",aliases=["Lehman Brothers","Lehman"]),
]}
json.dump(cur,open("tools/curated/new-entities-src.json","w",encoding="utf-8"),indent=1)
