package main

import (
	"encoding/hex"
	"errors"
	"strings"
	"time"

	"github.com/dgrijalva/jwt-go"
	"github.com/rs/zerolog/log"
)

type TokenGenerator struct{}

func NewTokenGenerator() *TokenGenerator {
	return &TokenGenerator{}
}

func (g TokenGenerator) GenerateToken(secretKey string) (string, error) {
	spltd := strings.Split(secretKey, ":")
	if len(spltd) != 2 {
		err := errors.New("wrong API KEY format")
		log.Err(err).Msg("wrong API KEY format provided via env variables")

		return "", err
	}

	keyID := spltd[0]
	signKey := spltd[1]

	iat := time.Now()
	claims := &jwt.StandardClaims{
		Audience:  "/admin/",
		ExpiresAt: iat.Add(time.Minute * 5).Unix(),
		IssuedAt:  iat.Unix(),
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	token.Header = map[string]interface{}{
		"kid": keyID,
		"alg": "HS256",
		"typ": "JWT",
	}

	sec, err := hex.DecodeString(signKey)
	if err != nil {
		return "", err
	}

	st, err := token.SignedString(sec)
	if err != nil {
		log.Err(err).Msg("signing token with api key error")
		return "", err
	}

	return st, nil
}