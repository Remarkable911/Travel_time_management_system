# 视图函数 放路由

from flask import Blueprint, render_template, request, redirect
from .models import *

blue=Blueprint('views',__name__)

