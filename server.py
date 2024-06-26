from fastapi import Depends, FastAPI, Response, status, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database import (get_db, Session)

from sqlalchemy.orm import Session
from fastapi import status
from fastapi.responses import JSONResponse

from models.models import User, Album, Review, Followers, Coment, Track, List
from schemas.user import UserSchema
from schemas.album import AlbumSchema
from schemas.review import ReviewSchema
from schemas.follower import FollowerSchema
from schemas.coment import ComentSchema
from schemas.track import TrackSchema
from schemas.list import ListSchema
from schemas.login_user import UserLoginSchema
from schemas.review_user import ReviewUserSchema


from typing import List

app = FastAPI()

origins = ['*', 'http://localhost:8000']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# pasta para images
app.mount("/imgs", StaticFiles(directory="static"), name="imgs")

# pasta static para o css
app.mount("/static", StaticFiles(directory="client/styles"), name="static")

# carregando templates com Jinja2
templates = Jinja2Templates(directory='client/templates')

## PROFILE =============================================================================

@app.get("/profile/{user_name}", response_class=HTMLResponse)
def get_album(request: Request, user_name: str, db: Session=Depends(get_db)):
    
    user: User = db.query(User).filter(User.user_name == user_name).first()
    user_id = user.id
    
    reviews: Review = db.query(Review).filter(Review.id_user == user_id).all()

    return templates.TemplateResponse("profile.html", {"request": request, "user_name": user_name, "reviews": reviews})

## ALBUM =============================================================================

# Rota para retornar um album pelo seu id
@app.get("/album/{album_id}/{user_name}", response_class=HTMLResponse)
def get_album(request: Request, album_id: int, user_name: str, db: Session=Depends(get_db)):
    
    album: Album = db.query(Album).filter(Album.id == album_id).first()
    user: User = db.query(User).filter(User.user_name == user_name).first()
    
    if not album:
        return "not found"
    
    reviews: Review = db.query(Review).filter(Review.id_album == album_id).all()
    users: User = db.query(User).all()
    
    return templates.TemplateResponse("album.html", {"request": request, "reviews": reviews, "album": album, "users": users, "user": user})

# Rota para cadastrar uma review a um album
@app.post("/album/{album_id}/{user_name}", response_class=RedirectResponse)
def post_review_album(request: Request, album_id: int, user_name: str, db: Session=Depends(get_db), form_data: ReviewUserSchema = Depends(ReviewUserSchema.as_form)):

    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")

    data = Review(**form_data.dict())
    db.query(Album).filter(Album.id == album_id).update({"reviews_number": Album.reviews_number + 1})

    user: User = db.query(User).filter(User.user_name == user_name).first()
    data.id_user = user.id

    data.id_album = album_id

    data.coments = 0
    data.likes = 0
    data.date_time = "2024"
    db.add(data)
    db.commit()
    
    return RedirectResponse(url=f"http://127.0.0.1:8000/home/"+ str(user_name), status_code=303)

## REVIEW ============================================================================

# Rota para retornar todos os comentários de uma review
@app.get("/coments/{review_id}")
def get_coments(review_id: int, db: Session=Depends(get_db)):
    data: List[Coment] = db.query(Coment).filter(Coment.id_review == review_id).all()    
    return data


# Rota para retornar uma review pelo id dela
@app.get("/review/{review_id}", response_class=HTMLResponse)
def get_review(request: Request, review_id: int, db: Session=Depends(get_db)):
    
    review: Review = db.query(Review).filter(Review.id == review_id).first()
    
    if not review:
        return "not found"
    
    user: User = db.query(User).filter(User.id == review.id_user).first()
    album: Album = db.query(Album).filter(Album.id == review.id_album).first()
    
    return templates.TemplateResponse("review.html", {"request": request, "review": review, "album": album, "user": user})

## HOME ========================================================================================================================
# Rota para renderizar a tela de cadastro com as reviews
@app.get("/home/{user_name}", response_class=HTMLResponse)
def render_home(request: Request, user_name: str, db: Session=Depends(get_db)):

    user_name = user_name
    reviews: Review = db.query(Review).all()
    users: User = db.query(User).all()
    albums: Album = db.query(Album).all()

    
    return templates.TemplateResponse("home.html", {"request": request, "reviews": reviews, "albums": albums, "users": users,"user_name": user_name})


## CADASTRO =====================================================================================================================
# Rota para renderizar a tela de cadastro
@app.get("/add_user", response_class=HTMLResponse)
def render_signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

# Rota para cadastrar um usuário no banco
@app.post("/add_user")
def add_user(request: Request, db: Session=Depends(get_db), form_data: UserSchema = Depends(UserSchema.as_form)):
    
    data = User(**form_data.dict())
    data.followers = 0
    data.following = 0
    data.reviews = 0
    db.add(data)
    db.commit()
    
    return templates.TemplateResponse("signup.html", {"request": request})

## LOGIN ========================================================================================================================
# Rota de login
@app.get("/login", response_class=HTMLResponse)
def render_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Rota que valida o login
@app.post("/login_user", response_class=RedirectResponse)
def valida_login(request: Request, db: Session=Depends(get_db), form_data: UserLoginSchema = Depends(UserLoginSchema.as_form)):

    aux_username: User = db.query(User).filter(User.user_name == form_data.username).first()

    if not aux_username:
        return "Username not found"       
    if aux_username:
        if aux_username.senha != form_data.senha:
            return "Senha Incorreta"
    
    return RedirectResponse(url=f"http://127.0.0.1:8000/home/"+ str(aux_username.user_name), status_code=303)

@app.get("/")
def show_devices():
    return {"SUCCESS"}


#rota pra mostrar todos os usuários cadastrados
@app.get("/user")
def get_filmes(db: Session=Depends(get_db)):
    data: List[User] = db.query(User).all()
    return data


#rota para procurar um usuário pelo nome na url
@app.get("/search_user/{user_name}")
def get_filmes(user_name: str, db: Session=Depends(get_db)):
    data: List[User] = db.query(User).filter(User.user_name == user_name).all()
    return data


#rota para retornar todos os álbuns cadastrados
@app.get("/album")
def get_albuns(db: Session=Depends(get_db)):
    data: List[Album] = db.query(Album).all()
    return data


#rota para cadastrar um álbum
@app.post("/add_album")
def add_album(album_schema: AlbumSchema, db: Session=Depends(get_db)):
    data = Album(**album_schema.dict())
    data.reviews_number = 0
    data.average_rating = 0
    data.tracks = 0
    db.add(data)
    db.commit()
    return ("OK")


#rota para buscar os seguidores de um usuário pelo id dele
@app.get("/followers/{user_id}")
def get_followers(user_id: int, db: Session=Depends(get_db)):
    data: List[Followers] = db.query(Followers).filter(Followers.id_user == user_id).all()
    data1 = []
    if not data:
        return "not found"
    for a in data:
        x = db.query(User).filter(User.id == a.id_follower).all()
        data1.append(x)
    return data1


#rota para adicionar um seguidor para um usuário 
#+ incrementa o número de followers do usuário
#+ incrementa o número de following do follower
@app.post("/add_follower")
def add_follower(follower_schema: FollowerSchema, db: Session=Depends(get_db)):
    data = Followers(**follower_schema.dict())
    db.query(User).filter(User.id == data.id_user).update({"followers": User.followers + 1})
    db.query(User).filter(User.id == data.id_follower).update({"following": User.following + 1})
    db.add(data)
    db.commit()
    return ("OK")


#rota para cadastrar um comentário
#+ incrementa o número de comentarios da review
@app.post("/add_coment")
def add_coment(coment_schema: ComentSchema, db: Session=Depends(get_db)):
    data = Coment(**coment_schema.dict())
    db.query(Review).filter(Review.id == data.id_review).update({"coments": Review.coments + 1})
    data.likes = 0
    db.add(data)
    db.commit()
    return ("OK")


#rota para retornar todas as tracks de um album
@app.get("/tracks/{album_id}")
def get_tracks(album_id: int, db: Session=Depends(get_db)):
    data: List[Track] = db.query(Track).filter(Track.id_album == album_id).all()    
    return data


#rota para cadastrar musicas em um album
#tem que passar uma lista no json dessa rota
@app.post("/add_tracks")
def add_tracks(track_schema: List[TrackSchema], db: Session=Depends(get_db)):
    data = [Track(**track.dict()) for track in track_schema]
    db.query(Album).filter(Album.id == data[0].id_album).update({"tracks": Album.tracks + 1})
    db.add_all(data)
    db.commit()
    return ("OK")


#rota para adicionar uma lista de musicas
# @app.post("/add_list")
# def add_list(list_schema: ListSchema, db: Session=Depends(get_db)):
#     data = List(**list_schema.dict())
#     db.query(Review).filter(Review.id == data.id_review).update({"coments": Review.coments + 1})
#     if not data.description:
#         data.description = " "
#     db.add(data)
#     db.commit()
#     return ("OK")