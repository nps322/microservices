
from app.schemas.pymodels import UserCreate,UserResponse

from app.models.user import User

from app.core.security import get_password_hash, verify_password, generate_jwt_token

from app.repositories.user import UserRepositories

from app.core.exception import UserAlreadyExistsException, WrongLoginOrPassword


class UserService():

    def __init__(self, repository:UserRepositories):

        self.repository = repository


    async def register_user(self, user:UserCreate) -> User:

        user_exists = await self.repository.get_by_email(user.email)
        
        if user_exists is not None:

            raise UserAlreadyExistsException(user.email)

        hash_password = get_password_hash(user.password)

        user_to_add = User(hashed_password= hash_password,
                           email= user.email,
                           user_name= user.user_name)

        result_user = await self.repository.create_user(user_to_add)
    
        return result_user
        

    async def login_user(self, email:str, password:str):

        cur_user = await self.repository.get_by_email(email)
        if not cur_user:
            raise  WrongLoginOrPassword
        

        if verify_password(password,cur_user.hashed_password):
            return generate_jwt_token(cur_user.id, cur_user.email)
        else:
            raise WrongLoginOrPassword
        

    async def get_user_by_email(self, email:str)  -> User | None:

        return await self.repository.get_by_email(email)